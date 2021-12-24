import functools
import importlib
from collections import namedtuple
from importlib import resources
import inspect

from typing import Dict

# Basic structure for storing information about one plugin
Plugin = namedtuple("Plugin", ("name", "cls"))

# Dictionary with information about all registered plugins
_PLUGINS :Dict = {}


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


def names_factory(package):
    """Create a names() function for one package"""
    return functools.partial(names, package)


def get_factory(package):
    """Create a get() function for one package"""
    return functools.partial(get, package)


def call_factory(package):
    """Create a call() function for one package"""
    return functools.partial(call, package)
