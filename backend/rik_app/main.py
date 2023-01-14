from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from .api.helpers import get_graphql_schema
from . import app_config
import uvicorn


# -------------------------------------------------------------------------------- #
debug = app_config.graphql.debug
app = Starlette(debug=debug)
schema = get_graphql_schema()
app.mount("/graphql", GraphQL(schema, debug=debug))
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.cors.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------------------------- #
if __name__ == "__main__":
    uvicorn.run("main:app", **app_config.uvicorn)
