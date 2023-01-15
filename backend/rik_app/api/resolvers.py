from ariadne import EnumType, QueryType
from rik_app.types import PersonType


# -------------------------------------------------------------------------------- #
enum = EnumType("PersonType", PersonType)
query = QueryType()


# -------------------------------------------------------------------------------- #
@query.field("searchCompanies")
def resolve_search_companies(_, info, pattern: str):
    return {
        "companies": [
            {
                "name": "Example Company",
                "tin": "12345678",
                "equity": 2500,
                "foundingDate": "2022-12-31",
                "shareholders": [
                    {
                        "name": "John Doe",
                        "tin": "12345678999",
                        "equity": 1000,
                        "founder": True,
                        "personType": PersonType.NATURAL
                    },
                    {
                        "name": "Jane Smith",
                        "tin": "98765432111",
                        "equity": 1500,
                        "founder": False,
                        "personType": PersonType.NATURAL
                    }
                ]
            }
        ]
    }


# -------------------------------------------------------------------------------- #
resolvers = [query, enum]
