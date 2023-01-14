from .utils import pathutils
from dotmap import DotMap
import tomli


# -------------------------------------------------------------------------------- #
path = pathutils.find_app_config_file(__file__)
app_config: DotMap
with open(path, "rb") as f:
    data = tomli.load(f)
    app_config = DotMap(data)
