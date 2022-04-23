from flask import Flask, request, render_template, make_response
from flask_restful import Resource, Api
from haystack.document_stores import FAISSDocumentStore
from haystack.pipelines import ExtractiveQAPipeline
from passage_retrieval import create_dpr

document_store = FAISSDocumentStore(sql_url= "sqlite:///haystack_test_faiss.db")
document_store.load(index_path="haystack_test_faiss", config_path="haystack_test_faiss_config")
retriever = create_dpr(document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True, progress_bar=False, top_k_per_candidate=2)
pipe = ExtractiveQAPipeline(reader, retriever)

app = Flask(__name__)

@app.route("/query")
def query(q):
    return pipe.run(query=q, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}})


if __name__ == '__main__':
    app.run(debug=True)