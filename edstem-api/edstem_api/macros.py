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


