# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import logging
import time

import common

from datadog_checks.snmp import SnmpCheck

log = logging.getLogger(__name__)


def test_test(spin_up_snmp, aggregator, check):
    metrics = common.SUPPORTED_METRIC_TYPES + common.UNSUPPORTED_METRICS
    instance = common.generate_instance_config(metrics)

    log.warning(instance)

    check.check(instance)


    for i in range(20):
        time.sleep(5)
        log.warning('metrics: {}'.format(aggregator._metrics))
        time.sleep(1)

    assert False
