from datetime import datetime, date, timedelta
from pydantic import validator, root_validator
from .judicial_person import JudicialPerson
from .shareholder import Shareholders
from copy import deepcopy
from dotmap import DotMap


# -------------------------------------------------------------------------------- #
class Company(JudicialPerson):
    """
    Pydantic object with field validations.
    Founding date validation can be temporarily disabled and re-enabled with
    the Company object class methods when generating dummy data for the database.
    Exceptions in validator methods are propagated up the execution stack
    by the @validator decorator as pydantic.ValidationError exceptions.
    """
    founding_date: date | str = None
    shareholders: Shareholders = None

    # ------------------------------------------------------------ #
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if hasattr(self, "founder"):  # pragma: no branch
            delattr(self, "founder")

    # ------------------------------------------------------------ #
    def to_dict(self) -> dict:
        copy = deepcopy(self)
        exclude = {"person_type", "field_id"}
        copy.shareholders = [sh.dict(exclude=exclude) for sh in self.shareholders]
        copy.founding_date = str(self.founding_date)
        return copy.dict(exclude=exclude)

    # ------------------------------------------------------------ #
    def to_dotmap(self) -> DotMap:
        return DotMap(self.to_dict())

    # ------------------------------------------------------------ #
    @classmethod
    def set_date_validation(cls, value: bool) -> None:
        cls.__date_validation__ = value

    # ------------------------------------------------------------ #
    @classmethod
    def enable_date_validation(cls) -> None:
        cls.__date_validation__ = True

    # ------------------------------------------------------------ #
    @classmethod
    def is_date_validation(cls) -> bool:
        return getattr(cls, "__date_validation__", True)

    # ------------------------------------------------------------ #
    @validator("founding_date", always=True)
    def validate_founding_date(cls, f_date: date | str | None) -> date:
        """
        This function validates that the founding date of a company is not in the
        future and not older than 30 days from the current date. If the founding date
        is a string, an attempt will be made to convert it into a date object.
        If no founding date is provided, current date is used instead.
        Skips date validation, if it has been disabled.

        :raises "date.empty-not-allowed": if no date is provided.
        :raises "date.invalid-format": if the date is a string and
            it cannot be converted into a date object.
        :raises "date.future-not-allowed": if the date is in the future.
        :raises "date.too-far-past": if the date is older than
            30 days from the current date.
        :param f_date: Company founding date.
        :return: Company founding date or current date.
        """
        if not cls.is_date_validation():
            return f_date
        if f_date is None:
            raise ValueError("date.empty-not-allowed")
        if isinstance(f_date, str):
            try:
                f_date = date.fromisoformat(f_date)
            except (TypeError, ValueError):
                raise ValueError("date.invalid-format")
        current_date = datetime.now().date()
        if f_date > current_date:
            raise ValueError("date.future-not-allowed")
        if f_date < (current_date - timedelta(days=30)):
            raise ValueError("date.too-far-past")
        return f_date

    # ------------------------------------------------------------ #
    @root_validator(pre=True, skip_on_failure=False)
    def validate_company_shareholders(cls, values: dict) -> dict:
        """
        This function validates that the equities of the shareholders
        of a company are equal to the equity of the company.

        :raises "shareholders.empty-not-allowed": if the shareholders list
            is either empty or nonexistent.
        :raises "shareholders.duplicates-not-allowed": if the shareholders list
            contains persons with identical TIN-s.
        :raises "shareholders.equity-mismatch": if the equities of the
            shareholders do not equal the equity of the company.
        :param values: Dict of all model fields.
        :return: List of shareholders.
        """
        shds: Shareholders = values.get("shareholders")
        if not shds:
            raise TypeError("shareholders.empty-not-allowed")
        tins = [sh.tin for sh in shds]
        if len(tins) != len(set(tins)):
            raise ValueError("shareholders.duplicates-not-allowed")
        if values.get("tin") in tins:
            raise ValueError("shareholders.self-company-not-allowed")
        names = [sh.name for sh in shds]
        if values.get("name") in names:
            raise ValueError("shareholders.self-company-not-allowed")
        shds_equity = sum([sh.equity for sh in shds])
        company_equity = values.get('equity', 0)
        if company_equity != shds_equity:
            raise ValueError("shareholders.equity-mismatch")
        return values

    # ------------------------------------------------------------ #
    @validator("equity", always=True)
    def validate_company_equity(cls, equity: int) -> int:
        """
        This function extends the base equity validation by validating
        that the equity of a Company is at least 2 500 units.

        :raises "equity.company-too-small": if equity is less than 2500.
        :param equity: Company equity, integer.
        :return: Company equity, unmodified.
        """
        if equity < 2500:
            raise ValueError("equity.company-too-small")
        return equity
