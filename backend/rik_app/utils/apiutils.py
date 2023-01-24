from .pathutils import find_graphql_schema_file
from rik_app.api.resolvers import resolvers
from ariadne import make_executable_schema
from ariadne import load_schema_from_path
from graphql import GraphQLSchema


# -------------------------------------------------------------------------------- #
def get_graphql_schema() -> GraphQLSchema:
    path = find_graphql_schema_file(__file__)
    type_defs = load_schema_from_path(str(path))
    return make_executable_schema(type_defs, *resolvers)
