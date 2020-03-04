import pytest
from rest_framework import test as drf_test

from cryptocurrency.blockchains import connectors, models


@pytest.fixture
def client():
    return drf_test.APIClient()


@pytest.fixture
def bitcoin_core_connector():
    return connectors.btc.BitcoinCoreConnector(
        rpc_username='bitcoin',
        rpc_password='qwerty54',
        rpc_host='http://example.com',
        rpc_port=18332,
    )


@pytest.fixture
def bitcoin_currency():
    currency = models.Currency.objects.create(name='BTC', min_confirmations=2)
    yield currency
    currency.delete()


@pytest.fixture
def bitcoin_core_node(bitcoin_currency):  # pylint: disable = redefined-outer-name  # yapf: disable
    node = models.Node.objects.create(
        name='bitcoin-core',
        currency=bitcoin_currency,
        is_default=True,
        rpc_username='bitcoin',
        rpc_password='qwerty54',
        rpc_host='example.com',
        rpc_port=18332,
    )
    yield node
    node.delete()