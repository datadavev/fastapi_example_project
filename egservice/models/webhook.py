
import typing
import pydantic
import github_webhooks.schemas

class PullRequestPayload(github_webhooks.schemas.WebhookCommonPayload, extra=pydantic.Extra.allow):
    class Pull(pydantic.BaseModel, extra=pydantic.Extra.allow):
        title: str
        url: str

    action: str
    pull_request: Pull

class PushPayload(pydantic.BaseModel, extra=pydantic.Extra.allow):
    class Pusher(pydantic.BaseModel, extra=pydantic.Extra.allow):
        name: str
        email: str

    class Sender(pydantic.BaseModel, extra=pydantic.Extra.allow):
        login: str

    ref: str
    before: str
    after: str
    pusher: Pusher
    sender: Sender

class PingPayload(pydantic.BaseModel, extra=pydantic.Extra.allow):

    event: str
    repository: str
    commit: str
    ref: str
    workflow: str
    requestID: str
