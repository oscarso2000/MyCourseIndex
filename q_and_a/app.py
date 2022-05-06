from flask import Flask, request, render_template, make_response
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import PDFToTextConverter, PreProcessor, FARMReader, DensePassageRetriever
from haystack.pipelines import ExtractiveQAPipeline
from pipeline import answer
# from passage_retrieval import create_dpr, joinParagraph
import pymysql
import json
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin_mci:mycourseindex-qa@database-qa.cp4ury9dboly.us-east-1.rds.amazonaws.com/qa_docstore'
app.config["input"] = "/data/input"
app.config["host"] = "0.0.0.0"

def create_dpr(document_store):
    retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
    max_seq_len_query=64,
    max_seq_len_passage=256,
    batch_size=16,
    use_gpu=True,
    embed_title=True,
    use_fast_tokenizers=True,
    )
    # document_store.update_embeddings(retriever)
    # document_store.save(index_path="haystack_test_faiss", config_path="haystack_test_faiss_config")
    # reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True, progress_bar=False, top_k_per_candidate=2)
   
    return retriever

def joinParagraph(str):
    s = str.replace('\n', ' ').replace('*', '').replace('%temp%', 'e').replace('```{code-cell} ocaml', '').replace('\ ', '').replace('`', '')
    return re.sub('\\\s',' ', s)

@app.route("/query_pipe",methods=['POST'])
def query_pipe():
    q=request.form['question']
    len_ans=int(request.form['lenans'])
    len_retriever=int(request.form['lenretr'])
    prediction = pipe.run(query=q, params={"Retriever": {"top_k": len_retriever}, "Reader": {"top_k": len_ans}})
    doc_ids = [prediction['answers'][i]['document_id'] for i in range(len_ans)]
    docs = document_store.get_documents_by_id(doc_ids)
    docs = [x.context for d in docs]
    ans = [prediction['answers'][i].answer for i in range(len_ans)]
    return json.dumps({
        'status':'success',
        'message': 'Process succesfully', 
        'result': ans,
        'context': docs})

@app.route("/query",methods=['POST'])
def query():
    q=request.form['question']
    len_ans=int(request.form['lenans'])
    len_retriever=int(request.form['lenretr'])
    context = retriever.retrieve(query=q, top_k=len_retriever)
    # prediction = pipe.run(query=q, params={"Retriever": {"top_k": len_retriever}, "Reader": {"top_k": len_ans}})
    ans = answer(1, context, q)
    return json.dumps({'status':'success','message': 'Process succesfully', 'result': ans})

@app.route('/')
def home():
    """Return a friendly HTTP greeting."""
    return 'Hello QNA API is running'

#endpoint to update embedded method
@app.route('/set_embed', methods=['POST'])
def set_embed():
    """Return a friendly HTTP greeting."""
    # document_store.write_documents()
    document_store.update_embeddings(retriever, update_existing_embeddings=False)
    document_store.save("haystack_test_faiss", "haystack_test_faiss_config")
    return json.dumps({'status':'Susccess','message': 'Sucessfully embeded method updated in FAISS Document', 'result': document_store.get_embedding_count()})

@app.route('/get_docs')
def get_docs():
    """Return a friendly HTTP greeting."""
    # document_store.write_documents()
    res=document_store.get_all_documents()[0].content
    return json.dumps({'status':'Susccess','message': 'Sucessfully embeded method updated in FAISS Document', 'result': res})


@app.route('/update_document', methods=['POST'])
def update_document():
    """Return a the url of the index document."""
    if request.files:
        # index is the target document where queries need to sent.
        index = request.form['index']
        # uploaded document for target source
        doc = request.files["doc"]

        file_path = os.path.join(app.config["input"], doc.filename)

        # saving the file to the input directory
        doc.save(file_path)
       
        # convert the pdf files into dictionary and update to ElasticSearch Document
        # dicts = convert_files_to_dicts(
        #     app.config["input"],
        #     clean_func=clean_wiki_text,
        #     split_paragraphs=False)
        
        converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])
        # doc_pdf = converter.convert(file_path=Path(f"{doc_dir}/3110.pdf"), meta=None)[0]
        doc_pdf = converter.convert(file_path=filepath, meta=None)[0]
        doc_pdf.content = join_Paragraph(doc_pdf.content)
        # doc_pdf = convert_pdf_to_string(file_path)
        preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=False,
        split_by="word",
        split_length=100,
        split_respect_sentence_boundary=True,
        )
        docs_default = preprocessor.process(doc_pdf)
        
        document_store.write_documents(dicts)
        os.remove(file_path)
        
        return json.dumps(
            {'status':'Susccess','message':
                'document available at http://'+ app.config["host"] +':'
                + app.config['SQLALCHEMY_DATABASE_URI'] +'/' + index + '/_search',
                'result': []})
    else:
        return json.dumps({'status':'Failed','message': 'No file uploaded', 'result': []})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    document_store = FAISSDocumentStore.load(index_path="haystack_test_faiss", config_path="haystack_test_faiss_config")
    retriever = create_dpr(document_store)
    reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True, progress_bar=True, return_no_answer=True)
    pipe = ExtractiveQAPipeline(reader, retriever)
    app.run(host=app.config["host"], port=port, debug=True)