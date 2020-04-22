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
import io

import pytest
from django.core import management

from django_obm import models


@pytest.mark.django_db
def test_command():
    out = io.StringIO()
    management.call_command("initnodes", stdout=out)
    assert models.Node.objects.all().count() > 0
    assert "successfully" in out.getvalue()