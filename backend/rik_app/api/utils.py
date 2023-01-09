from pathlib import Path
from rik_app import app_config


# -------------------------------------------------------------------------------- #
def get_schema_file_path() -> Path:
    file_name = app_config.graphql.schema_file_name
    path: Path | None = None
    for i in range(0, 4):
        path = Path(__file__).parents[i].joinpath(file_name).resolve()
        if path.exists() and path.is_file():
            break
    if not path or not path.exists():
        raise RuntimeError("Unable to find GraphQL schema file.")
    return path
