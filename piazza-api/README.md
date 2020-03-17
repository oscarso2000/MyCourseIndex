# Piazza API package
<!-- Put AZURE badge here -->
Unofficial Client for Piazza's Internal API

## Installation

```
$ poetry add piazza-api
```

## Usage

```python
>>> from piazza_api import Piazza
>>> p = Piazza()
>>> p.user_login(email= ..., pass=...)
Successful Login

>>> cs4300 = p.course("k5h3t0fy1gm5vv")

>>> cs4300.get_post("str")
...

>>> posts = cs4300.iter_all_posts(limit=10)
>>> for post in posts:
...     call_function(post)

```

Above are some examples to get started; more in the documentation.