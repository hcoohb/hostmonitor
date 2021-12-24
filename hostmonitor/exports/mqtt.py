from plugins import register_class


@register_class
class export_mqtt:
    def __init__(self) -> None:
        print("Export MQTT loaded")

    def export(self, data):
        print(self)
        print(data)
