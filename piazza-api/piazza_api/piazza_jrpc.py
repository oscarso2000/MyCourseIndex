"""Piazza RPC is the lower level API module.

This module maps directly to Piazza's lower level API and will contain most/all
breaking changes if their API changes.

They seem to use JSON-RPC which is the remote procedure call protocol. It is a
different method than REST since we have to specify methods and arguments
"""

import json
import requests
import six.moves
import uuid

from piazza_api.exceptions import (
    AuthenticationError,
    NotAuthenticatedError,
    PiazzaRequestError
)


class PiazzaJRPC(object):
    """PiazzaJRPC is the unofficial client for Piazza's internal API.
    
    This module maps directly to Piazza's lower level API and will contain most/all
    breaking changes if their API changes.

    They seem to use JSON-RPC which is the remote procedure call protocol. It is a
    different method than REST since we have to specify methods and arguments
    
    :param class_id: This is the ID of the class from which to query posts
    :type object: str or None

    Example:
        >>> p = PiazzaRPC("hl5qm84dl4t3x2")
        >>> p.user_login("mb2363@cornell.edu", "PASSWORD")
        >>> p.content_get(181)
            ...
    
    .. note: One could directly use this instead of the Piazza class, however
        the Piazza class offers a nice wrapper
    """
    def __init__(self, class_id=None):
        self._cid = class_id
        self.base_api_urls = {
            "logic": "https://piazza.com/logic/api",
        }
        self.session = requests.Session()
    

    def user_login(self, email, password):
        """user_login grabs a session cookie using email and password.
        
        :param email: Email used for authentication
        :type email: str
        :param password: Password used for authentication
        :type password: str
        """
        login_data = {
            "method": "user.login",
            "params": {
                "email": email,
                "pass": password
            }
        }

        r = self.session.post(
            self.base_api_urls["logic"],
            data=json.dumps(login_data),
        )

        if r.json()["result"] not in ["OK"]:
            raise AuthenticationError(
                "Could not authenticate.\n{}".format(r.json())
            )
    

    def request(self, method, data=None, class_id=None,class_id_key="nid",
                api_url="logic"):
        """request gets the data from an arbitrary Piazza API endpoint.
        
        TODO: Write a more in-depth explanation
        
        :param method: [description]
        :type method: [type]
        :param data: [description], defaults to None
        :type data: [type], optional
        :param class_id: [description], defaults to None
        :type class_id: [type], optional
        :param class_id_key: [description], defaults to "nid"
        :type class_id_key: str, optional
        :param api_url: [description], defaults to "logic"
        :type api_url: str, optional
        """
        self._check_authenticated()

        cid = class_id if class_id else self._cid
        if data is None:
            data = {}
        
        headers = {}
        if "session_id" in self.session.cookies:
            headers["CSRF-Token"] = self.session.cookies["session_id"]
        
        endpoint = self.base_api_urls[api_url]
        if api_url == "logic":
            endpoint += "?method={}&aid={}".format(
                method,
                uuid.uuid4()
            )
        
        response = self.session.post(
            endpoint,
            data=json.dumps(
                {
                    "method": method,
                    "params": dict({class_id_key: cid}, **data)
                }
            ),
            headers=headers
        )

        return response.json()
    

    def fetch_content(self, content_id, course_id=None):
        """fetch_content grabs the post content for a content id in a course.

        :param content_id: The post id that we want to fetch
        :type content_id: str
        :param course_id: This is the id of the course we query
        :type course_id: str, optional
        :returns: Object containing all of the post data
        :rtype: dict
        """
        r = self.request(
            method="content.get",
            data={"cid": content_id},
            class_id=course_id
        )

        return self._handle_error(r, "Could not get post {}.".format(content_id))
    

    def get_all_postings(self, limit=150, offset=20, sort="updated", cid=None):
        """get_all_posts returns all posts from Piazza.
        
        :param limit: number of posts to fetch starting from offset,
            defaults to 150
        :type limit: int, optional
        :param offset: offset starting from post 0 (bottom), defaults to 20
        :type offset: int, optional
        :param sort: How to sort posts; only known value is "updated",
            defaults to "updated"
        :type sort: str, optional
        :param cid: ID of the course that we are fetching posts from,
            defaults to None
        :type cid: str, optional
        """

        r = self.request(
            method="network.get_my_feed",
            class_id=cid,
            data=dict(
                limit=limit,
                offset=offset,
                sort=sort
            )
        )
        return self._handle_error(r, "Could not retrieve all posts.")

    # Private Methods below

    def _check_authenticated(self):
        """_check_authenticated checks the user is logged in and raises errors.
        
        :returns: None
        :rtype: None
        :raises NotAuthenticatedError: if user is not authenticated
        """
        if not self.session.cookies:
            raise NotAuthenticatedError("You must authenticate before making" +
                " any requests.")
        
        return None
    

    def _handle_error(self, result, err_msg):
        """_handle_error checks for error in requests and notifies caller
        
        [extended_summary]
        
        :param result: Response body
        :type result: dict
        :param err_msg:  The message given to the :class:`RequestError`
            instance raised
        :type err_msg: str
        :returns: Returns the response result
        :rtype: str
        :raises RequestError: If result has error
        """
        if result.get('error'):
            raise PiazzaRequestError("{}\nResponse Body: {}".format(
                err_msg,
                json.dumps(result, indent=4)
            ))
        else:
            return result.get("result")
