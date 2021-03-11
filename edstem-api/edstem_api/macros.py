""""""

import api


def get_courses(username=None, password=None):
    user_data = api.request(
        endpoint="user",
        username=username,
        password=password,
    )

    courses = user_data["courses"]
    course_data = []

    for record in courses:
        # check if student?
        # if record["role"]["role"] == "student"
        course_record = record["course"]
        course_code = course_record["code"]
        course_session = course_record["session"]
        course_id = course_record["id"]
        course_year = course_record["year"]
        course_name = course_record["name"]
        course_data.append(
            {
                "course_code": course_code,
                "course_session": course_session,
                "course_id": course_id,
                "course_year": course_year,
                "course_name": course_name,
            }
        )

    return course_data


def get_course_id(course_name, course_term, username=None, password=None):
    user_data = api.request(
        endpoint="user",
        username=username,
        password=password,
    )

    courses = user_data["courses"]

    course_session = None
    course_year = None
    if course_term is not None:

        # Parse session
        # if course_term[0] == "F":
        #     course_session = "Fall"
        # elif course_term[0] == "S":
        #     course_session = "Spring"

        # Parse year
        course_year = course_term[1:]

    course_ids = []

    for record in courses:
        course_data = record["course"]

        if course_name and course_name != course_data["code"]:
            continue

        # if course_session and course_session != course_data["session"]:
        #     continue

        if course_year and course_year != course_data["year"]:
            continue

        course_ids.append(course_data["id"])

    if len(course_ids) == 1:
        return course_ids[0]


def invite_one(course_id, name, email, tutorial, role="student", username=None, password=None):
    result = api.request(
        endpoint="courses/{}/invite".format(course_id),
        json={
            "invites": [
                {
                    "name": name,
                    "email": email,
                    "tutorial": tutorial
                }
            ],
            "role": role
        },
        username=username,
        password=password,
    )

    return result is not None


def invite_many(course_id, users, role="student", username=None, password=None):
    result = api.request(
        endpoint="courses/{}/invite".format(course_id),
        json={
            "invites": users,
            "role": role
        },
        username=username,
        password=password,
    )

    return result is not None


def unenroll(course_id, user_ids, username=None, password=None):
    result = api.request(
        endpoint="courses/{}/unenroll".format(course_id),
        json={
            "user_ids": user_ids
        },
        username=username,
        password=password,
    )

    return result is not None


def users(course_id, username=None, password=None):
    result = api.request(
        endpoint="courses/{}/admin".format(course_id),
        username=username,
        password=password,
    )

    if "users" in result:
        return result.get("users", [])

def get_feed(course_id, limit=-1, sort="date", order="desc", username=None, password=None):
    """
    """
    if limit > -1:
        result = api.request(
            endpoint=f"courses/{course_id}/threads?sort={sort}&order={order}",
            username=username,
            password=password,
        )
    else:
        result = api.request(
            endpoint=f"courses/{course_id}/threads?limit={limit}&sort={sort}&order={order}",
            username=username,
            password=password,
        )
    return result


def get_thread_content(thread_id, username=None, password=None):
    result = api.request(
        endpoint=f"threads/{thread_id}",
        username=username,
        password=password,
        )
    return result


def simplify_thread_info(thread: dict) -> dict:
    """Disseminates a thread into useful, easy-to-understand information.

    Args:
        thread (dict): JSON-styled dict representing a thread.
    
    Returns:
        dict: Simplified thread with the useful info.
    """

    def recurse_on_post(f, post: dict, **kwargs) -> dict:
        """
        We define a simple helper function here, to recurse through the entire 
        post "tree" structure and apply any post-changing functions to the post.
        Very helpful for dealing with nested answers and comments of a thread.

        Args:
            f (dict -> dict): Function to be applied to the post.
            post (dict): JSON-styled dict representing any general post.
            **kwargs (Any): Named arguments to pass to the function f.

        Returns:
            post: The updated post after processing with f(post, **kwargs)
        """
        post = f(post, **kwargs)

        if "answers" in post:
            new_answers = []
            for answer in post["answers"]:
                new_answer = recurse_on_post(f, answer, **kwargs)
                new_answers.append(new_answer)
            post["answers"] = new_answers

        if "comments" in post:
            new_comments = []
            for comment in post["comments"]:
                new_comment = recurse_on_post(f, comment, **kwargs)
                new_comments.append(new_comment)
            post["comments"] = new_comments

        return post

    def simplify_post(post: dict, keys: set) -> dict:
        """Slice a subset of the original post contents with the keys we want.

        Args:
            post (dict): JSON-styled dict representing any general post.
            keys (set): A set of keys to include in the new post.

        Returns:
            dict: The new post with select keys.
        """
        return {x: post[x] for x in post if x in keys}

    def map_ids_to_names(post: dict, users: list) -> dict:
        """Exchange meaningless numbers with actual names of people.

        Args:
            post (dict): JSON-styled dict representing any general post.
            users (list): JSON-styled list of user objects, each with a name.

        Returns:
            dict: The new post with user ids changed to names.
        """
        user_id = post["user_id"]
        for user in users:
            if user["id"] == user_id:
                post["user_id"] = user["name"]
                # Rename the key (and preserve dict order) for clarity
                post = {"by" if k == "user_id" else k:v for k,v in post.items()}
                break

        return post
    

    def strip_html(post: dict) -> dict:
        """Get rid of ugly HTML tags in our post content.

        Args:
            post (dict): JSON-styled dict of a post with content to filter.

        Returns:
            dict: The new post without any HTML in the content parameter.
        """
        from re import sub
        new_content = sub('<[^<]+?>', '', post["content"])
        post["content"] = new_content
        return post

    # Now our helpers simplify our job to a few lines!

    # Set of keys to include in the new thread dict
    useful_keys = {"user_id", "title", "content", "created_at", "answers", "comments"}

    # Simplify the thread without the junk
    new_thread = recurse_on_post(simplify_post, post=thread["thread"], keys=useful_keys)
    
    # Give users names
    even_newer_thread = recurse_on_post(map_ids_to_names, post=new_thread, users=thread["users"])

    # Bye bye HTML tags
    the_newest_thread = recurse_on_post(strip_html, post=even_newer_thread)

    return the_newest_thread
