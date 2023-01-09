from ariadne import make_executable_schema
from ariadne import load_schema_from_path
from .utils import get_schema_file_path
from .resolvers import resolvers

path = get_schema_file_path()
type_defs = load_schema_from_path(str(path))
schema = make_executable_schema(type_defs, *resolvers)
