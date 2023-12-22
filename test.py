from xknx import XKNX
from xknx.io import ConnectionConfig, ConnectionType

async def telegram_received_cb(telegram):
    print(f'Telegram received: {telegram}')


async def try_address(addr):
    connection_config = ConnectionConfig(connection_type=ConnectionType.AUTOMATIC, gateway_ip=addr)
    xknx = XKNX(telegram_received_cb=telegram_received_cb, daemon_mode=True, connection_config=connection_config)
    try:
        await xknx.start()
    except Exception as e:
        print(e)
        await xknx.stop()
