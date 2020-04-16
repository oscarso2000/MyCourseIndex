from .piazza_jrpc import PiazzaJRPC
from .course import Course


class Piazza(object):
    """Piazza is an object that represent the Piazza website.

    Since this represents the website, we only offer login and returning course
    methods which then allow the user a lower level access to the Piazza
    website and the information contained within.

    :param piazza_jrpc: Piazza RPC lower level API
    :type piazza_jrpc: :class:`~piazza_api.piazza_jrpc.PiazzaJRPC`
    """
    def __init__(self, piazza_jrpc=None):
        self._jrpc_api = piazza_jrpc if piazza_jrpc else None
    

    def user_login(self, email, password):
        """Login with email, password and get back a session cookie

        :param email: The email used for authentication
        :type  email: str
        :param password: The password used for authentication
        :type  password: str
        """
        self._jrpc_api = PiazzaJRPC()
        self._jrpc_api.user_login(email=email, password=password)
    

    def course(self, course_id):
        """course returns :class:`Course` instance for ``course_id``
        
        :param course_id: This is the ID of the Course.
            This can be found by visiting your class page
            on Piazza's web UI and grabbing it from
            https://piazza.com/class/{course_id}
        :type course_id: str
        :returns: Course instance that allows accessing posts etc.
        :rtype: :class:`~piazza_api.course.Course`
        """
        self._ensure_authenticated()
        return Course(course_id, self._jrpc_api.session)
    
    def _ensure_authenticated(self):
        self._jrpc_api._check_authenticated()