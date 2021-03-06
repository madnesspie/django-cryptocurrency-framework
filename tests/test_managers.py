# Copyright 2019-2020 Alexander Polishchuk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys

import pytest

from django_obm import models


@pytest.mark.integration
class TestNodeManagerIntegration:
    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures("bitcoin_core_node", "geth_node")
    def test_fetch_recent_transactions():
        txs = models.Node.objects.fetch_recent_transactions(limit=5)
        # Because there are two nodes in the database
        assert len(txs) <= 5 * 2
        for tx in txs:
            assert isinstance(tx, models.Transaction)

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures("bitcoin_core_node", "geth_node")
    def test_bulk_create_recent_transactions():
        # Calls twice to check that method ignores conflicts
        models.Node.objects.bulk_create_recent_transactions(limit=1)
        txs = models.Node.objects.bulk_create_recent_transactions(limit=5)
        for tx in txs:
            queryset = models.Transaction.objects.filter(txid=tx.txid)
            assert queryset.count() == 1
            tx_from_db = queryset.first()
            assert tx_from_db
            assert isinstance(tx_from_db.pk, int)

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures(
        "bitcoin_core_node", "geth_node"
    )
    def test_sync_transactions(bitcoin_transaction):
        txs = models.Node.objects.sync_transactions(recent_limit=5)
        # One tx exists and 5 for each node will added
        assert len(txs) == 11
        bitcoin_transaction.refresh_from_db()
        assert bitcoin_transaction.block_number is not None
        # Tests txs order
        prev_block = txs[0].block_number
        for tx in txs:
            block_number = tx.block_number or sys.maxsize
            assert block_number <= prev_block
            prev_block = block_number


@pytest.mark.integration
class TestTransactionManagerIntegration:
    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures("bitcoin_transaction")
    def test_sync():
        txs = models.Transaction.objects.sync()
        assert isinstance(txs, list)
        assert len(txs) == 1
        assert txs[0].block_number is not None
