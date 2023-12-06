import hashlib
import hmac
import typing
import fastapi
import pydantic

hook_app = fastapi.FastAPI()

@hook_app.middleware("http")
async def verify_signature(request: fastapi.Request, call_next): # payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    signature_header = request.headers.get("x-hub-signature-256", None)
    if not signature_header:
        raise fastapi.HTTPException(status_code = 403, detail="x-hub-signature-256 header is missing!")
    secret_token = "my secret"
    payload_body = await request.body()
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        raise fastapi.HTTPException(status_code = 403, detail="Request signatures didn't match!")
    response = await call_next(request)
    return response

class Data(pydantic.BaseModel, extra=pydantic.Extra.allow):

    class Extra(pydantic.BaseModel, extra=pydantic.Extra.allow):
        key: typing.Optional[str]

    event: str
    repository: str
    commit: str
    ref: str
    head: typing.Optional[str]
    workflow: typing.Optional[str]
    requestID: str
    data: Extra


@hook_app.post("/hook", include_in_schema=False)
async def redirect_docs(data:Data):
    return data
