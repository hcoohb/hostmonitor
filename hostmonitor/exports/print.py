from plugins import register_class
print("importing PRINT")

@register_class
class export_print:
    def __init__(self) -> None:
        print("Export PRINT loaded")

    def export(self, data):
        print(data)
