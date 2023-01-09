from ariadne import QueryType

query = QueryType()
resolvers = [query]


# -------------------------------------------------------------------------------- #
@query.field("searchCompanies")
def resolve_search_companies(*_):
    return "Hello!"
