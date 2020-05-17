"""Authentication Module for the GraphQL Api"""

from flask import request
from functools import wraps
import cryptography
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
import jwt
import requests
import typing
import logging


res = requests.get(
    "https://login.microsoftonline.com/5d7e4366-1b9b-45cf-8e79-b14b27df46e1/.well-known/openid-configuration"
    # "https://login.microsoftonline.com/common/.well-known/openid-configuration"
)
JWKS_URI = res.json()["jwks_uri"]
res = requests.get(JWKS_URI)
JWK_KEYS = res.json()


SCOPES = {
    "User": ["Q1MgNDMwMAo=", "SU5GTyAxOTk4Cg==", "View"],
    "Developer": ["Q1MgNDMwMAo=", "SU5GTyAxOTk4Cg==", "View"]
}

def make_scope_assignments(
    scopes: typing.Mapping[str, typing.Sequence[str]]
) -> typing.Callable[[str], typing.Set[str]]:
    def get_scopes_for_role(role: str) -> typing.Set[str]:
        nonlocal scopes
        granted_scopes = set()
        [granted_scopes.add(scope) for scope in scopes[role]]
        return granted_scopes

    return get_scopes_for_role


def verify_token(
    token: str,
    app_id: str,
    get_scopes_for_role: typing.Callable[[str], typing.Set[str]]
    ) -> dict:
    if token == "null" or not token:
        return {"scope": "Unauthorized"}  # Don't accept empty tokens
    token_header = jwt.get_unverified_header(str(token))
    # logger.info(token_header)

    x5c = None

    for key in JWK_KEYS["keys"]:
        if (
            key["kid"] == token_header["kid"]
        ):  # Get the certificate specified in the JWT
            x5c = key["x5c"]  # We will use it to verify the signature
    cert = "".join(
        ["-----BEGIN CERTIFICATE-----\n", x5c[0], "\n-----END CERTIFICATE-----\n"]
    )
    public_key = load_pem_x509_certificate(
        cert.encode(), default_backend()
    ).public_key()
    # logger.info(public_key.public_bytes(cryptography.hazmat.primitives.serialization.Encoding.PEM, cryptography.hazmat.primitives.serialization.PublicFormat.SubjectPublicKeyInfo))
    try:
        claims = jwt.decode(  # This will return the claims only if the signature is valid.
            token, public_key, algorithms="RS256", audience=app_id
        )
        # {
        #  upn: user identity,
        #  roles: ["role a", "role b"],
        #  firstname: "foo",
        #  lastname: "bar"
        # }
    except jwt.ExpiredSignatureError:

        # Signature Has Expired, return unauthorized scope.
        return {"scope": "Unauthorized", "reason": "Token signature expired"}
    except jwt.InvalidSignatureError:
        return {
            "scope": "Unauthorized",
            "reason": "Token signature cannot be verified",
        }
    
    # logger.info("Claims: {}".format(claims))
    
    roles = claims.get("roles", None)
    # logger.debug("Roles: {}".format(str(roles)))
    auth_claims = {}
    auth_claims["sub"] = claims["upn"]  # Provide the user identity with the claim
    if not roles:  # A role needs to be provided for authentication to work
        auth_claims["scope"] = "Unauthorized"
    else:
        scopes = set()
        for role in roles:  # Sometimes more than one role can be provided.
            scopes.update(get_scopes_for_role(role))
        if not scopes:
            auth_claims["scope"] = "Unauthorized"
        else:
            auth_claims["scope"] = list(scopes)
    return auth_claims


def get_name(token: str, app_id: str) -> str:
    """Get the name from the JWT.

    :param access_token: Access token
    """
    if token == "null" or not token:
        return {"scope": "Unauthorized"}  # Don't accept empty tokens
    token_header = jwt.get_unverified_header(str(token))
    # logger.info(token_header)

    x5c = None

    for key in JWK_KEYS["keys"]:
        if (
            key["kid"] == token_header["kid"]
        ):  # Get the certificate specified in the JWT
            x5c = key["x5c"]  # We will use it to verify the signature
    cert = "".join(
        ["-----BEGIN CERTIFICATE-----\n", x5c[0], "\n-----END CERTIFICATE-----\n"]
    )
    public_key = load_pem_x509_certificate(
        cert.encode(), default_backend()
    ).public_key()
    # logger.info(public_key.public_bytes(cryptography.hazmat.primitives.serialization.Encoding.PEM, cryptography.hazmat.primitives.serialization.PublicFormat.SubjectPublicKeyInfo))
    try:
        claims = jwt.decode(  # This will return the claims only if the signature is valid.
            token, public_key, algorithms="RS256", audience=app_id
        )
        # {
        #  upn: user identity,
        #  roles: ["role a", "role b"],
        #  firstname: "foo",
        #  lastname: "bar"
        # }
    except jwt.ExpiredSignatureError:

        # Signature Has Expired, return Unknown.
        return "Unknown User"
    except jwt.InvalidSignatureError:
        return "Unknown User"
    
    # logger.info("Claims: {}".format(claims))
    
    name = claims.get("given_name", "User")
    # logger.info(name)
    return name


def get_claims(access_token, app_id):
    get_scopes_for_role = make_scope_assignments(SCOPES)
    return verify_token(access_token, app_id, get_scopes_for_role)


def user_jwt_required(access_token, app_id):
    """
    A function to protect a Flask endpoint.

    If you decorate an endpoint with this, it will ensure that the requester
    has a valid access token before allowing the endpoint to be called. This
    does not check the freshness of the access token.
    """

    get_scopes_for_role = make_scope_assignments(SCOPES)
    auth_claims = verify_token(access_token, app_id, get_scopes_for_role)

    # logger.info("Reason: {}".format(auth_claims.get("reason", "None Given")))

    # logger.critical(auth_claims["scope"] == "Unauthorized")
    # logger.critical("Scopes: {}".format(auth_claims["scope"]))

    if (auth_claims["scope"] == "Unauthorized"):
        return False
    else:
        return ("View" in auth_claims["scope"])  
