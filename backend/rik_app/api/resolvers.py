from ariadne import EnumType, QueryType
from rik_app.tax_id import TINPerson


# -------------------------------------------------------------------------------- #
enum = EnumType("PersonType", TINPerson)
query = QueryType()


# -------------------------------------------------------------------------------- #
@query.field("searchCompanies")
def resolve_search_companies(_, info, pattern: str):
    return {
        "companies": [
            {
                "name": "Example Company",
                "tin": "1234567890",
                "equity": 100,
                "foundingDate": "2023-01-12",
                "shareholders": [
                    {
                        "name": "John Doe",
                        "tin": "0987654321",
                        "equity": 50,
                        "founder": True,
                        "personType": TINPerson.NATURAL
                    },
                    {
                        "name": "Jane Smith",
                        "tin": "1111111111",
                        "equity": 25,
                        "founder": False,
                        "personType": TINPerson.NATURAL
                    }
                ]
            }
        ]
    }


# -------------------------------------------------------------------------------- #
resolvers = [query, enum]
