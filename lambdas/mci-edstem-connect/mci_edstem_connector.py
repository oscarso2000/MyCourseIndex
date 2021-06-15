import macros
import requests
from elasticsearch import Elasticsearch
import time
from datetime import datetime, timezone

basic_auth = (
    "", # NOTE: Replace with computer generated auth
    "",
)

edstem_ids = []
edstem_email = "help@mycourseindex.com"
edstem_password = "" # NOTE: Replace with password
macros.api.get_auth_token(edstem_email, edstem_password)

update_interval=1

clusterIP = "" # NOTE: Replace with HTTPS location

es_indices = [""] # NOTE: Place index names here
es_indices = {k: v for k, v in zip(edstem_ids, es_indices)}

es = Elasticsearch(clusterIP, http_auth=basic_auth)

def recurse_on_post(post: dict, **kwargs):
    cur_time = datetime.strptime(post["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z").astimezone(timezone.utc).replace(tzinfo=None)
    min_time = cur_time

    if "answers" in post:
        for answer in post["answers"]:
            new_time = recurse_on_post(answer, **kwargs)
            if new_time > min_time:
                min_time = new_time

    if "comments" in post:
        for comment in post["comments"]:
            new_time = recurse_on_post(f, comment, **kwargs)
            if new_time > min_time:
                min_time = new_time

    return min_time

def get_latest_posts(feed,latest_duration=update_interval):
    latest_posts = []
    current_time = datetime.utcnow()

    for post in feed:
        post_updated = datetime.strptime(post["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z").astimezone(timezone.utc).replace(tzinfo=None)
        #post_updated = recurse_on_post(post) #datetime.strptime(post["modified"], "%Y-%m-%dT%H:%M:%SZ")
        post_age = (current_time - post_updated).total_seconds()
        post_age_in_minutes = post_age / 60
        if post_age_in_minutes < latest_duration:
            latest_posts.append(post)

    return latest_posts


def check_for_new_posts(class_id):
    feed = macros.get_feed(class_id, username=edstem_email, password=edstem_password)["threads"]
    updates = get_latest_posts(feed)
    print(len(updates))
    ids = [t["id"] for t in updates]
    updates = [macros.get_thread_content(i) for i in ids]
    updates = [macros.simplify_thread_info(t) for t in updates]
    for u, i in zip(updates, ids):
        u["doctype"] = "EdStem"
        u["url"] = f"https://edstem.org/us/courses/{class_id}/discussion/{i}"
        es.update(
            index=es_indices[class_id],
            id=f"EdStem-{i}",
            body={
                "doc_as_upsert": True,
                "doc": u,
            },
            refresh=True,
        )
    print(f"{len(updates)} updates completed")

    return


def update_handler(event, context):
    for cid in edstem_ids:
        check_for_new_posts(cid)

