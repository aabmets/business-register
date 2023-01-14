from ariadne import make_executable_schema
from ariadne import load_schema_from_path
from rik_app.utils import pathutils
from graphql import GraphQLSchema
from .resolvers import resolvers


# -------------------------------------------------------------------------------- #
def get_graphql_schema() -> GraphQLSchema:
    path = pathutils.find_graphql_schema_file(__file__)
    type_defs = load_schema_from_path(str(path))
    return make_executable_schema(type_defs, *resolvers)
