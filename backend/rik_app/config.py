from rik_app.utils.pathutils import find_app_config_file
from rik_app.utils.classutils import SingletonMeta
from dotmap import DotMap
import tomli


# -------------------------------------------------------------------------------- #
class ConfigSingleton(metaclass=SingletonMeta):
    """
    This class is a singleton which contains the app configuration.
    The data is loaded from file on very first instantiation and
    further calls return a deepcopy of the initial instance.
    """
    graphql: DotMap
    uvicorn: DotMap
    postgres: DotMap
    cors: DotMap

    # ------------------------------------------------------------ #
    def __init__(self, **_):
        path = find_app_config_file(__file__)
        with open(path, "rb") as f:
            data = tomli.load(f)
            for k, v in data.items():
                setattr(self, k, DotMap(v))


# -------------------------------------------------------------------------------- #
ConfigSingleton(should_clone=True)  # initialize the config as clones
