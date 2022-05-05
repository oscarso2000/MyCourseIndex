from flask import Flask, request, render_template, make_response
# from haystack.document_stores import FAISSDocumentStore
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.document_stores.es_converter import elasticsearch_index_to_document_store
from haystack.nodes import ElasticsearchRetriever, EmbeddingRetriever
from haystack.pipelines import ExtractiveQAPipeline
from passage_retrieval import create_dpr

# document_store = FAISSDocumentStore(sql_url= "sqlite:///haystack_test_faiss.db")
# document_store.load(index_path="haystack_test_faiss", config_path="haystack_test_faiss_config")

cluster_ip = "https://es.mci.mycourseindex.com" 
# cluster_ip = "http://18.191.198.23:9200"

document_store = ElasticsearchDocumentStore(
    host = cluster_ip,
    scheme="https",
    api_key_id="mciesaccess",
    api_key="$apr1$0jnrOVl.$jS2m8nwTlkXkoJHMNq2RQ/"
)




basic_auth = (
    "$apr1$0jnrOVl.$jS2m8nwTlkXkoJHMNq2RQ/",
    "mciesoscar",
)

# new_ds = elasticsearch_index_to_document_store(
#     document_store=empty_document_store,
#     original_content_field="content",
#     original_index_name="document",
#     original_name_field="title",
#     preprocessor=preprocessor,
#     port=cluster_ip,
#     verify_certs=False,
#     scheme="https",
#     username="mciesaccess",
#     password="$apr1$0jnrOVl.$jS2m8nwTlkXkoJHMNq2RQ/"
# )

retriever = create_dpr(document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True, progress_bar=False, top_k_per_candidate=2)
pipe = ExtractiveQAPipeline(reader, retriever)

app = Flask(__name__)

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
@app.route('/set_embeded', methods=['POST'])
def set_embeded():
    """Return a friendly HTTP greeting."""
    # document_store.write_documents()
    document_store.update_embeddings(retriever)
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
        dicts = convert_files_to_dicts(
            app.config["input"],
            clean_func=clean_wiki_text,
            split_paragraphs=False)
        
        document_store.write_documents(dicts)
        os.remove(file_path)
        return json.dumps(
            {'status':'Susccess','message':
                'document available at http://'+ app.config["host"] +':'
                + app.config["port"] +'/' + index + '/_search',
                'result': []})
    else:
        return json.dumps({'status':'Failed','message': 'No file uploaded', 'result': []})

if __name__ == '__main__':
    app.run(debug=True)