# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import pytest
import time

from datadog_checks.dev import docker_run

HERE = os.path.dirname(os.path.abspath(__file__))
COMPOSE_DIR = os.path.join(HERE, 'docker')

@pytest.fixture(scope='session', autouse=True)
def spin_up_envoy():
    flavor = os.getenv('FLAVOR', 'default')

    with docker_run(
        os.path.join(COMPOSE_DIR, flavor, 'docker-compose.yaml')
    ):
        time.sleep(5)
        yield
