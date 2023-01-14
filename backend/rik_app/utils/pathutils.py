from pathlib import Path


# -------------------------------------------------------------------------------- #
def file_finder(ref: str, file_name: str) -> Path:
    path: Path | None = None
    for i in range(0, 4):
        path = Path(ref).parents[i].joinpath(file_name).resolve()
        if path.exists() and path.is_file():
            break
    if not path or not path.exists():
        raise RuntimeError(f"Unable to find file: {file_name}")
    return path

    
# -------------------------------------------------------------------------------- #
def find_graphql_schema_file(ref: str) -> Path:
    return file_finder(ref, "schema.graphql")


# -------------------------------------------------------------------------------- #
def find_app_config_file(ref: str) -> Path:
    return file_finder(ref, "app.config.toml")


# -------------------------------------------------------------------------------- #
__all__ = [
    "file_finder",
    "find_graphql_schema_file",
    "find_app_config_file"
]
