from butter.mas.api import ClientFactory

# connect to KIP using butter HTTP connector
class ButterConnector:
    class __ButterConnector:
        def __init__(self, ip, connection_protocol='tcp'):
            self.butterHttpClient = ClientFactory().getClient(ip, protocol=connection_protocol)

        def __str__(self):
            return repr(self) + self.butterHttpClient

    instance = None

    def __init__(self, ip, connection_protocol='tcp'):
        if not ButterConnector.instance:
            ButterConnector.instance = ButterConnector.__ButterConnector(ip, connection_protocol)

    def __getattr__(self, name):
        return getattr(self.instance, name)