import plugins

print("### I am from exports")

registered = plugins.names_factory(__package__)
get = plugins.get_factory(__package__)