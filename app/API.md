# API for the backend of the application

**Note**: THis is a work in progress and nowhere near complete

`/courses`: Uses to retrieve the courses that the user is in
- request body: JSON
    - ``token``: User's auth token (can be fetched using the getToken method)
    - EX:
    ```json
    {
        "token": "TOKEN HERE"
    }
    ```
- returns: list of objects as follows:
    - EX:
    ```json
    [
        {
            "protected": true,
            "courseName": "CS 4300"
        },
        {
            "protected": false,
            "courseName": "INFO 1998"
        }
    ]
    ```
`/tokeVerify`: Used to verify that the piazza token is correct
- request body: JSON
    - ``token``: User's auth token (can be fetched using the getToken method)
    - ``courseName``: Name of the course to be checked
    - ``piazzaToken``: password the user input for the piazza token
    - EX:
    ```JSON
    {
        "token": "LONG TOKEN HERE",
        "courseName": "CS 4300",
        "piazzaToken": "12345"
    }
    ```
- returns: String of OK or NO
    - EX: "OK"

