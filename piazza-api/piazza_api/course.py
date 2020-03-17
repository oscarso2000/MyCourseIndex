from collections import namedtuple
from .piazza_jrpc import PiazzaJRPC


# Course

class Course(object):
    """Course represents a course on Piazza
    
    :param class_id: ID of the class
    :type class_id: str
    :param session: object containing cookies used for
        authentication
    :type session: requests.Session
    """
    def __init__(self, class_id, session):
        self._cid = class_id
        self._jrpc = PiazzaJRPC(class_id = class_id)
        self._jrpc.session = session

        # eventually add feed filters


    def get_post(self, content_id):
        """Get data from post `cid`.

        :param content_id: This is the post ID to get
        :type  content_id: str
        :returns: Dictionary with all data on the post
        :rtype: dict
        """
        return self._jrpc.fetch_content(content_id=content_id)

    
    def get_postings(self, limit=100, offset=0):
        """Get your feed for this network.
        
        Pagination for this can be achieved by using the `limit` and
        `offset` params

        :param limit: Number of posts from feed to get, starting from `offset`
        :type limit: int
        :param offset: Offset starting from bottom of feed
        :type offset: int
        :returns: Feed metadata, including list of posts in feed format; this
            means they are not the full posts but only in partial form as
            necessary to display them on the Piazza feed. For example, the
            returned dicts only have content snippets of posts rather
            than the full text.
        :rtype: dict
        """
        return self._jrpc.get_all_postings(limit=limit, offset=offset)
    

    def iter_all_posts(self, limit=100):
        """iter_all_posts returns an iter for the posts visible to the user.
        
        This grabs the sidebar feed and the correspinding ids; each post must
        then be individually fetched. There does not seem to be a bulk endpoint
        :(. This is a warning as to how this function works in case of weird
        behavior.
        
        :param limit: Number of posts from feed to get, defaults to 100
        :type limit: int, optional
        :returns: An iterator which yields all posts which the current user
            can view
        :rtype: generator
        """
        feed = self.get_postings(limit=None, offset=0)
        cids = [post['id'] for post in feed["feed"]]
        if limit:
            limit = min(limit, len(cids))
            cids = cids[:limit]
        
        for cid in cids:
            yield self.get_post(cid)

    

