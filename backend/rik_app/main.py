from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from rik_app.utils.apiutils import get_graphql_schema
from rik_app.config import ConfigSingleton
from rik_app.db import DatabaseSingleton
import uvicorn
import asyncio
import sys


# -------------------------------------------------------------------------------- #
config = ConfigSingleton()
debug = config.graphql.debug
app = Starlette(debug=debug)
schema = get_graphql_schema()
app.mount("/graphql", GraphQL(schema, debug=debug))
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=config.cors.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------------------------- #
async def main():
    db = DatabaseSingleton()
    await db.initialize()
    uvi_config = uvicorn.Config("main:app", **config.uvicorn)
    server = uvicorn.Server(uvi_config)
    await server.serve()


# -------------------------------------------------------------------------------- #
if __name__ == "__main__":
    if sys.platform == 'win32':  # pragma: no branch
        policy = asyncio.WindowsSelectorEventLoopPolicy()
        asyncio.set_event_loop_policy(policy)
    asyncio.run(main())
