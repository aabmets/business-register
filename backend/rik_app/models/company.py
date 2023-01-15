from datetime import datetime, date, timedelta
from pydantic import validator, root_validator
from .judicial_person import JudicialPerson
from .shareholder import Shareholders


# -------------------------------------------------------------------------------- #
class Company(JudicialPerson):
    """
    Pydantic object with field validations.
    Founding date validation can be temporarily disabled by functions
    in the gentools module when generating dummy data for the database.
    Exceptions in validator methods are propagated up the execution stack
    by the @validator decorator as pydantic.ValidationError exceptions.
    """
    founding_date: date | str = None
    shareholders: Shareholders = None

    # ------------------------------------------------------------ #
    @classmethod
    def disable_date_validation(cls) -> None:
        cls.__date_validation__ = False

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
    def validate_founding_date(cls, f_date: date | str) -> date:
        """
        This function validates that the founding date of a company is not in the
        future and not older than 30 days from the current date. If the founding date
        is a string, an attempt will be made to convert it into a date object.
        If no founding date is provided, current date is used instead.
        Skips date validation, if it has been disabled.

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
            return datetime.now().date()
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
    @validator("equity", pre=True, always=True)
    def inject_equity(cls, equity: int) -> int:
        return equity  # for shareholders validation

    # ------------------------------------------------------------ #
    @validator("shareholders", always=True)
    def validate_shareholders(cls, shds: Shareholders, values: dict) -> Shareholders:
        """
        This function validates that the equities of the shareholders
        of a company are equal to the equity of the company.

        :raises "shareholders.empty-not-allowed": if the shareholders list
            is either empty or nonexistent.
        :raises "shareholders.equity-mismatch": if the equities of the
            shareholders do not equal the equity of the company.
        :param shds: List of shareholders.
        :param values: Dict of previously validated fields.
        :return: List of shareholders.
        """
        if not shds:
            raise TypeError("shareholders.empty-not-allowed")
        shds_equity = sum([sh.equity for sh in shds])
        company_equity = values.get('equity', 0)
        if company_equity != shds_equity:
            raise ValueError("shareholders.equity-mismatch")
        return shds

    # ------------------------------------------------------------ #
    @root_validator()
    def validate_company_equity(cls, values: dict) -> dict:
        """
        This function extends the base equity validation by validating
        that the equity of a Company is at least 2 500 units.

        :raises "equity.too-small": if equity is less than 2 500.
        :param values: Dict of all previously validated fields.
        :return: Company equity, unmodified.
        """
        equity = values.get("equity")
        if isinstance(equity, int) and equity < 2500:
            raise ValueError("equity.too-small")
        return values
