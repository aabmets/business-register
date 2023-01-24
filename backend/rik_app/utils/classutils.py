from copy import deepcopy
from dotmap import DotMap


# -------------------------------------------------------------------------------- #
class SingletonMeta(type):
    """
    Metaclass for creating singleton classes.
    Optionally providing the "should_clone" kwarg as True on
    the very first instantiation will make any further calls
    return a deepcopy of the original instance.
    """
    __instances = {}

    # ------------------------------------------------------------ #
    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            should_clone = kwargs.pop("should_clone", False)
            instance = super().__call__(*args, **kwargs)
            cls.__instances[cls] = DotMap(
                should_clone=should_clone,
                instance=instance,
            )
        instance = cls.__instances[cls]
        if instance.should_clone:
            return deepcopy(instance.instance)
        return instance.instance

    # ------------------------------------------------------------ #
    @classmethod
    def purge_instance(mcs, cls: object):
        mcs.__instances.pop(cls, None)
