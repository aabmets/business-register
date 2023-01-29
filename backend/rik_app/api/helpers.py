from rik_app.models import Shareholder, Company
from pydantic import ValidationError
from typing import Any


# -------------------------------------------------------------------------------- #
class ErrorsList(list):
    """
    This class is used for storing and converting
    errors raised by Ariadne mutation resolvers.
    """
    # ------------------------------------------------------------ #
    def __call__(self, field_id: str, message: str) -> None:
        self.append({
            "field_id": field_id,
            "message": message,
        })

    # ------------------------------------------------------------ #
    def to_dict(self):
        return {
            "result": False,
            "errors": list(self)
        }


# -------------------------------------------------------------------------------- #
def data_message(data: Any) -> dict:
    return {"result": True, "data": data}


# -------------------------------------------------------------------------------- #
def error_message(message: str) -> dict:
    return {"result": False, "error": message}


# -------------------------------------------------------------------------------- #
def process_incoming_data(data: dict, errors: ErrorsList, validate_date=True, set_founders=True) -> Company | None:
    parsed_shds = []
    for sh in data.pop("shareholders", []):
        field_id = sh.get("field_id", None)  # GraphQL schema asserts field_id
        try:
            if set_founders:
                sh["founder"] = True
            parsed_sh = Shareholder(**sh)  # this raises validation errors
            parsed_shds.append(parsed_sh)
        except ValidationError as ex:
            for e in ex.errors():
                errors(field_id, e["msg"])
    data["shareholders"] = parsed_shds

    field_id = data.get("field_id", None)  # GraphQL schema asserts field_id
    try:
        Company.set_date_validation(validate_date)
        valid_company = Company(**data)  # this raises validation errors
        Company.enable_date_validation()
        return valid_company
    except ValidationError as ex:
        for e in ex.errors():
            errors(field_id, e["msg"])
    finally:
        Company.enable_date_validation()
    return None


# -------------------------------------------------------------------------------- #
__all__ = [
    "ErrorsList",
    "data_message",
    "error_message",
    "process_incoming_data",
]
