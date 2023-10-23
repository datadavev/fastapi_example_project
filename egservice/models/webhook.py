
import pydantic
import github_webhooks.schemas

class PullRequestPayload(github_webhooks.schemas.WebhookCommonPayload):
    class Pull(pydantic.BaseModel):
        title: str
        url: str

    action: str
    pull_request: Pull

class PushPayload(github_webhooks.schemas.WebhookCommonPayload):
    class Push(pydantic.BaseModel):
        title: str
        url: str

    action: str
    push_request: Push
