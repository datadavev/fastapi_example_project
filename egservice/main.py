"""
Example FastAPI application

This example FastAPI application includes:

* configuration override with environment variables
* logging to JsonL
"""
import hashlib
import hmac
import logging
import sys
import typing

import fastapi
import fastapi.middleware
import fastapi.middleware.cors
import fastapi.staticfiles
import fastapi.templating

import json_logging

#import github_webhooks
#import github_webhooks.schemas
import pydantic

import egservice
import egservice.config
import egservice.log_middleware
import egservice.webhook

# Setup access logging
#L = egservice.log_middleware.get_logger()

app = fastapi.FastAPI(
    secret_token=None,
    title="EgFastAPI",
    description=__doc__,
    version=egservice.__version__,
    contact={"name": "Dave Vieglais", "url": "https://github.com/datadavev/"},
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/license/mit/",
    },
    openapi_url="/api/v1/openapi.json",
    docs_url="/api",
)

json_logging.init_fastapi(enable_json=True)
json_logging.init_request_instrument(app)

logger = logging.getLogger("example")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stderr))

# Enables CORS for UIs on different domains
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "HEAD",
    ],
    allow_headers=[
        "*",
    ],
)

# Add the logger
#app.add_middleware(
#    egservice.log_middleware.LogMiddleware,
#    logger=L,
#)


# static files and templates
app.mount(
    "/static",
    fastapi.staticfiles.StaticFiles(directory=egservice.config.settings.static_dir),
    name="static",
)

templates = fastapi.templating.Jinja2Templates(
    directory=egservice.config.settings.template_dir
)

'''
@app.hooks.register("pull_request", egservice.models.webhook.PullRequestPayload)
async def pr_handler(payload:egservice.models.webhook.PullRequestPayload) -> None:
    print(f'New pull request {payload.pull_request.title}')
    print(f'  link: {payload.pull_request.url}')
    print(f'  author: {payload.sender.login}')


@app.hooks.register("push", egservice.models.webhook.PushPayload)
async def push_handler(payload: egservice.models.webhook.PushPayload) -> None:
    print(f'New push {payload}')

@app.hooks.register("ping", egservice.models.webhook.PingPayload)
async def push_handler(payload: egservice.models.webhook.PingPayload) -> None:
    print(f'New ping {payload}')
'''

app.mount(
    "/hook",
    egservice.webhook.hook_app
)

@app.get("/", include_in_schema=False)
async def redirect_docs(request: fastapi.Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "meta": {"version": egservice.__version__}}
    )




# Ignore requests for favicon
@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    raise fastapi.HTTPException(status_code=404, detail="Not found")


if __name__ == "__main__":
    # Start the service when run from the command line
    try:
        import uvicorn
        uvicorn.run(
            #"main:app",
            app,
            port=egservice.config.settings.port,
            host=egservice.config.settings.host,
            #reload=True,
            log_config=None,
        )
    except ImportError as e:
        print("Unable to run as uvicorn is not available.")
        print(e)
