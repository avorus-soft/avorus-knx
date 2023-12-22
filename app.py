import os
import ssl

import asyncclick as click

from api import Api
from knx import KNX
from mqtt_client import Client
from misc import logger


class App:
    def __init__(self, client):
        self.api = Api()
        self.client = client

    def setup(self):
        self.locations = self.api.get('/api/').json()['locations']
        self.knx = KNX(self.client, self.locations)

    async def start(self):
        await self.knx.start()

    async def reload(self):
        await self.knx.stop()
        self.setup()
        await self.start()


@click.command()
@click.option('--ca_certificate', default='/opt/tls/ca_certificate.pem')
@click.option('--client_certificate', default='/opt/tls/client_certificate.pem')
@click.option('--client_key', default='/opt/tls/client_key.pem')
async def main(ca_certificate, client_certificate, client_key):
    ssl_context = ssl.create_default_context(cafile=ca_certificate)
    ssl_context.load_cert_chain(
        client_certificate, client_key)
    async with Client(
            os.environ['MQTT_HOSTNAME'],
            client_id='knx',
            port=8883,
            keepalive=60,
            tls_context=ssl_context,
            max_concurrent_outgoing_calls=2000
    ) as client:
        await client.subscribe('api/data-refresh')
        app = App(client)
        app.setup()
        await app.start()
        async with client.messages() as messages:
            async for message in messages:
                if message.topic.matches('api/data-refresh'):
                    logger.info('Reload signal received.')
                    await app.reload()


if __name__ == '__main__':
    main()
