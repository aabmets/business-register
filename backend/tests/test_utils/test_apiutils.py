from rik_app.utils.apiutils import get_graphql_schema
from graphql import GraphQLSchema


# -------------------------------------------------------------------------------- #
def test_get_graphql_schema():
    schema = get_graphql_schema()
    assert isinstance(schema, GraphQLSchema)
