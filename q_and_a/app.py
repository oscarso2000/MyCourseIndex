from flask import Flask, request, render_template, make_response
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import PDFToTextConverter, PreProcessor, FARMReader, DensePassageRetriever
from haystack.pipelines import ExtractiveQAPipeline
from passage_retrieval import create_dpr, joinParagraph
import pymysql
import json
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin_mci:mycourseindex-qa@database-qa.cp4ury9dboly.us-east-1.rds.amazonaws.com/qa_docstore'
app.config["input"] = "/data/input"
app.config["host"] = "0.0.0.0"

document_store = FAISSDocumentStore(sql_url= app.config['SQLALCHEMY_DATABASE_URI'], faiss_index_factory_str="Flat",return_embedding=True)
# document_store.load(index_path="haystack_test_faiss", config_path="haystack_test_faiss_config")
# document_store = FAISSDocumentStore.load(index_path="my_faiss_index.faiss", config_path="my_faiss_index.json")
retriever = create_dpr(document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True, progress_bar=False, top_k_per_candidate=2)
pipe = ExtractiveQAPipeline(reader, retriever)



@app.route("/query")
def query(q):
    prediction = pipe.run(query=q, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}})
    ans = [prediction['answers'][i].answer for i in range(len_ans)]
    return json.dumps({'status':'success','message': 'Process succesfully', 'result': answer})

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
    return json.dumps({'status':'Susccess','message': 'Sucessfully embeded method updated in ElasticSearch Document', 'result': []})

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
        #initialization of the Haystack Elasticsearch document storage
       
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
    app.run(host=app.config["host"], port=port, debug=True)