from pathlib import Path
from dotmap import DotMap
import tomli


# -------------------------------------------------------------------------------- #
path = Path().cwd().joinpath("app_config.toml")
app_config: DotMap
with open(path, "rb") as f:
    data = tomli.load(f)
    app_config = DotMap(data)
