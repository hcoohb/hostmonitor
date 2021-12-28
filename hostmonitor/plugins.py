import functools
import importlib
from collections import namedtuple
from importlib import resources
import inspect

from typing import Dict, List

# Basic structure for storing information about one plugin
Plugin = namedtuple("Plugin", ("name", "cls"))

# Dictionary with information about all registered plugins
_PLUGINS: Dict = {}


def register(func):
    """Decorator for registering a new plugin"""
    package, _, plugin = func.__module__.rpartition(".")
    print(f"Module prop: {func.__module__.rpartition('.')}")
    print("Func data:")
    print(dir(func.__module__))
    print(f"class data is : {inspect.getmembers(func.__module__, inspect.isclass)}")
    # t = getattr( inspect.getmembers(func.__module__, inspect.isclass)[0][1],type_attr)
    # print(f"init the class is : {t}")
    pkg_info = _PLUGINS.setdefault(package, {})
    pkg_info[plugin] = Plugin(name=plugin, func=func)
    return func


def register_class(cls):
    # print(dir(cls))
    # print(cls.__name__)
    package, _, plugin = cls.__module__.rpartition(".")
    pkg_info = _PLUGINS.setdefault(package, {})
    pkg_info[plugin] = Plugin(name=plugin, cls=cls)
    return cls


def names(package):
    """List all plugins in one package"""
    _import_all(package)
    print(f"NAMES: {_PLUGINS}")
    return sorted(_PLUGINS[package])


def get(package, plugin):
    """Get the class for a given plugin"""
    _import(package, plugin)
    return _PLUGINS[package][plugin].cls


def call(package, plugin, *args, **kwargs):
    """Call the given plugin"""
    plugin_func = get(package, plugin)
    return plugin_func(*args, **kwargs)


def _import(package, plugin):
    """Import the given plugin file from a package"""
    importlib.import_module(f"{package}.{plugin}")


def _import_all(package):
    """Import all plugins in a package"""
    files = resources.contents(package)
    plugins = [f[:-3] for f in files if f.endswith(".py") and f[0] != "_"]
    print(f"FILES: {plugins}")
    for plugin in plugins:
        _import(package, plugin)


def required_args(package, plugin) -> List:
    """Return a list of required argument when instancing the plugin"""
    cls = get(package, plugin)
    args_no_default = [
        p.name
        for p in inspect.signature(cls.__init__).parameters.values()
        if p.name != "self"
        and p.default is p.empty
        and p.kind != p.VAR_POSITIONAL
        and p.kind != p.VAR_KEYWORD
    ]
    # print(f"{plugin} parameters: {args_no_default}")
    return args_no_default


def validate_args(package, plugin, args) -> bool:
    """Ensure the plugin class can be instanciated with given args"""
    args_req = required_args(package, plugin)
    validated = True
    args_missing = [arg for arg in args_req if arg not in args]
    if len(args_missing) > 0:
        print(
            f"Could not load plugin '{plugin}' as parameters {args_missing} is/are missing"
        )
        return False
    return True


def names_factory(package):
    """Create a names() function for one package"""
    return functools.partial(names, package)


def get_factory(package):
    """Create a get() function for one package"""
    return functools.partial(get, package)


def call_factory(package):
    """Create a call() function for one package"""
    return functools.partial(call, package)


def required_args_factory(package):
    return functools.partial(required_args, package)


def validate_args_factory(package):
    return functools.partial(validate_args, package)
