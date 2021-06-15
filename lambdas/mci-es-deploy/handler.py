try:
    import unzip_requirements
except ImportError:
    pass

import json

from auth import (
    get_claims
)
from query_config import (
    query_template,
    basic_auth,
    create_presigned_url,
)

from elasticsearch import Elasticsearch

MCI_APP_ID = "41e533e7-b473-4087-86a1-c00f86b39487"

# claim_to_class = {
#     "C1-SP2021": "cs_4300_sp2021",
#     "C2-SP2021": "cs_4780_sp2021"
# }
cluster_ip = "https://es.mci.mycourseindex.com" 
# cluster_ip = "http://18.191.198.23:9200"

es = Elasticsearch(cluster_ip, http_auth=basic_auth)
# es = Elasticsearch(cluster_ip)

def search(event, context):
    try:
        body = json.loads(event['body'])
        course = body["course"]
        query = body["query"]
        token = body["access_token"]

        claims = get_claims(token, MCI_APP_ID)

        print("Claims retrieved")

        if claims['scope'] == "Unauthorized":
            response = {
                "statusCode": 403,
                "headers": {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    "Access-Control-Allow-Credentials": True
                },
                "body": json.dumps({
                    "access": "Not Authorized",
                    "message": "Not authorized to access any resource."
                }),
                "isBase64Encoded": False
            }
            print("Claim invalid")
        else:
            print("Has some scope....")
            results = None
            for claim in claims['scope']:
                if claim == course:
                    print("REQ being made")
                    # Make request to ES
                    query_template["query"]["query_string"]["query"] = query
                    search_response = es.search(index =  claim, body=query_template)
                    print("Retrieved search hits")
                    hits = search_response["hits"]["hits"]
                    results = []
                    for hit in hits:
                        src = hit["_source"]
                        src["highlight"] = hit["highlight"]
                        if src["doctype"] == "video":
                            # If Video, get timestamps
                            timestamps = json.loads(src["timestamps"])
                            times = []
                            print(src["title"])
                            for key in src["highlight"]:
                                for highlight in src["highlight"][key]:
                                    h = highlight.replace("<em>", "").replace("</em>", "")
                                    hit_index = src["content"].lower().find(h.lower())
                                    print(h.lower())
                                    print(f"Hit index: {hit_index}")
                                    if hit_index != -1:
                                        hours, minutes, seconds = timestamps[str(hit_index)]
                                        times.append(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
                            src["timestamps"] = sorted(times)

                            # If Video, Generate pre-signed URL for Video
                            src["videoUrl"] = create_presigned_url("mci-video-lectures", src["s3location"], expiration=3660)

                        results.append(src)
                    
                    response = {
                        "statusCode": 200,
                        "headers": {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*',
                            "Access-Control-Allow-Credentials": True
                        },
                        "body": json.dumps({
                            "access": "Authorized",
                            "message": f'There are {search_response["hits"]["total"]} hits',
                            "results": json.dumps({"hits": results}),
                        })
                    }
            if results is None:
                response = {
                    "statusCode": 403,
                    "headers": {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        "Access-Control-Allow-Credentials": True
                    },
                    "body": json.dumps({
                        "access": "Not Authorized",
                        "message": "Not authorized to access this resource."
                    })
                }
    except Exception as e:
        response =  {
            "statusCode": 500,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({"error": repr(e)})
        }

    print("About to return")

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
