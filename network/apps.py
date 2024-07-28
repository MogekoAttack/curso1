from django.apps import AppConfig


class NetworkConfig(AppConfig):
    name = 'network'

    def signal_register(self):
        import network.signals