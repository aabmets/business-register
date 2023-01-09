from starlette.applications import Starlette
from ariadne.asgi import GraphQL
from rik_app import app_config
from api import schema
import uvicorn

debug = app_config.graphql.debug
app = Starlette(debug=debug)
app.mount("/graphql", GraphQL(schema, debug=debug))


if __name__ == "__main__":
    uvicorn.run("main:app", **app_config.uvicorn)
