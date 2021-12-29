import socket
import string
from typing import Dict, List, Union

import paho.mqtt.client as paho
from hostmonitor.plugins import register_class

WHITELIST = "_-" + string.ascii_letters + string.digits
SUBSTITUTE = "_"


def whitelisted(s, whitelist=WHITELIST, substitute=SUBSTITUTE):
    parts = [part for part in s.split("/") if part != ""]
    for i in range(len(parts)):
        parts[i] = "".join(c if c in whitelist else substitute for c in parts[i])
    return "/".join(parts)


@register_class
class export_mqtt:
    def __init__(self, host, port=1883, prefix: str = "") -> None:
        print("Export MQTT loaded")
        self.host = host
        self.port = int(port)
        self.client = None
        self.prefix = whitelisted(prefix + "/" + socket.gethostname())

    def export(self, data):
        print(f"trying to publish to mqtt with: {data}")
        if not self.client:
            self.init_mqtt()

        for topic, value in self.convert_to_topics(data).items():
            try:
                pub = self.client.publish(topic, value, qos=1)
                print(f"On {topic}, val: {value}")
                # pub.wait_for_publish()# blocks until message is published
            except Exception as e:
                print("Can not export stats to MQTT server (%s)" % e)

    def init_mqtt(self):
        """Init the connection to the MQTT server."""
        try:
            self.client = paho.Client(
                client_id="monitor_" + socket.gethostname(), clean_session=False
            )
            # client.username_pw_set(username=self.user, password=self.password)
            self.client.connect(host=self.host, port=self.port)
            self.client.loop_start()
        except Exception as e:
            self.client = None
            print("Connection to MQTT server failed : %s " % e)

    def convert_to_topics(self, data: Dict) -> Dict:
        """Take the data dict and convert to a dict with topic:value"""

        def to_topics(
            str_prefix: str,
            data_dict,
            str_join: str = "/",
        ) -> Dict:

            values = {}
            if isinstance(data_dict, dict):
                for k, v in data_dict.items():
                    new_prefix = str_prefix + str_join + whitelisted(str(k))
                    values.update(to_topics(new_prefix, v, str_join))
            elif isinstance(data_dict, list):
                for val in data_dict:
                    values[str_prefix] = val
            else:
                values[str_prefix] = data_dict
            return values

        return to_topics(self.prefix, data)
