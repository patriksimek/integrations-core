# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

import logging
import time

import common

from datadog_checks.snmp import SnmpCheck

log = logging.getLogger(__name__)


# def test_command_generator(aggregator):
#     """
#     Command generator's parameters should match init_config
#     """
#     check = SnmpCheck('snmp', common.MIBS_FOLDER, {}, {})
#     cmdgen, _, _, _, _, _, _ = check._load_conf(common.SNMP_CONF)
#
#     # Test command generator MIB source
#     mib_folders = cmdgen.snmpEngine.msgAndPduDsp\
#         .mibInstrumController.mibBuilder.getMibSources()
#     full_path_mib_folders = map(lambda f: f.fullPath(), mib_folders)
#
#     assert "/etc/mibs" in full_path_mib_folders
#     assert not cmdgen.ignoreNonIncreasingOid
#
#     # Test command generator `ignoreNonIncreasingOid` parameter
#     check = SnmpCheck('snmp', common.IGNORE_NONINCREASING_OID, {}, {})
#     cmdgen, _, _, _, _, _, _ = check._load_conf(common.SNMP_CONF)
#     assert cmdgen.ignoreNonIncreasingOid

# def test_type_support(spin_up_snmp, aggregator, check):
#     """
#     Support expected types
#     """
#     metrics = common.SUPPORTED_METRIC_TYPES + common.UNSUPPORTED_METRICS
#     instance = common.generate_instance_config(metrics)
#
#     check.check(instance)
#
#
#     log.warning(aggregator._metrics)
#     # service_checks = aggregator._service_checks
#     #
#     # self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 1, RESULTS_TIMEOUT)
#
#     for k, v in aggregator._metrics.iteritems():
#         log.warning('{}: {}'.format(k,v))
#
#     # Test metrics
#     for metric in common.SUPPORTED_METRIC_TYPES:
#         metric_name = "snmp." + metric['name']
#         aggregator.assert_metric(metric_name, tags=common.CHECK_TAGS, count=1)
#     for metric in common.UNSUPPORTED_METRICS:
#         metric_name = "snmp." + metric['name']
#         aggregator.assert_metric(metric_name, tags=common.CHECK_TAGS, count=0)
#
#     # Test service check
#     aggregator.assert_service_check("snmp.can_check", status=SnmpCheck.OK,
#                                     tags=common.CHECK_TAGS, at_least=1)
#
#     aggregator.all_metrics_asserted()


# def test_snmpget(spin_up_snmp, aggregator, check):
#     """
#     When failing with 'snmpget' command, SNMP check falls back to 'snpgetnext'
#
#         > snmpget -v2c -c public localhost:11111 1.3.6.1.2.1.25.6.3.1.4
#         iso.3.6.1.2.1.25.6.3.1.4 = No Such Instance currently exists at this OID
#         > snmpgetnext -v2c -c public localhost:11111 1.3.6.1.2.1.25.6.3.1.4
#         iso.3.6.1.2.1.25.6.3.1.4.0 = INTEGER: 4
#     """
#     instance = common.generate_instance_config(common.PLAY_WITH_GET_NEXT_METRICS)
#
#     check.check(instance)
#
#     common.wait_for_async(check, aggregator)
#
#     # Test service check
#     aggregator.assert_service_check("snmp.can_check", status=SnmpCheck.OK,
#                                     tags=common.CHECK_TAGS, at_least=1)
#
#     check.check(instance)
#     common.wait_for_async(check, aggregator)
#
#     # Test metrics
#     for metric in common.PLAY_WITH_GET_NEXT_METRICS:
#         metric_name = "snmp." + metric['name']
#         aggregator.assert_metric(metric_name, tags=common.CHECK_TAGS, count=1)
#
#     # Test service check
#     aggregator.assert_service_check("snmp.can_check", status=SnmpCheck.OK,
#                                     tags=common.CHECK_TAGS, count=1)
#
#     aggregator.all_metrics_asserted()

#
# def test_scalar(self):
#     """
#     Support SNMP scalar objects
#     """
#     config = {
#         'instances': [self.generate_instance_config(self.SCALAR_OBJECTS)]
#     }
#     self.run_check_n(config, repeat=3)
#     self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 1, RESULTS_TIMEOUT)
#
#     # Test metrics
#     for metric in self.SCALAR_OBJECTS:
#         metric_name = "snmp." + (metric.get('name') or metric.get('symbol'))
#         self.assertMetric(metric_name, tags=self.CHECK_TAGS, count=1)
#
#     # Test service check
#     self.assertServiceCheck("snmp.can_check", status=AgentCheck.OK, tags=self.CHECK_TAGS, at_least=1)
#
#     self.coverage_report()
#
#
# def test_table(self):
#     """
#     Support SNMP tabular objects
#     """
#     config = {
#         'instances': [self.generate_instance_config(self.TABULAR_OBJECTS)]
#     }
#     self.run_check_n(config, repeat=3, sleep=2)
#     self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 1, RESULTS_TIMEOUT)
#
#     # Test metrics
#     for symbol in self.TABULAR_OBJECTS[0]['symbols']:
#         metric_name = "snmp." + symbol
#         self.assertMetric(metric_name, at_least=1)
#         self.assertMetricTag(metric_name, self.CHECK_TAGS[0], at_least=1)
#
#         for mtag in self.TABULAR_OBJECTS[0]['metric_tags']:
#             tag = mtag['tag']
#             self.assertMetricTagPrefix(metric_name, tag, at_least=1)
#
#     # Test service check
#     self.assertServiceCheck("snmp.can_check", status=AgentCheck.OK,
#                             tags=self.CHECK_TAGS, at_least=1)
#
#     self.coverage_report()
#
#
# def test_table_v3_MD5_DES(self):
#     """
#     Support SNMP V3 priv modes: MD5 + DES
#     """
#     config = {
#         'instances': []
#     }
#
#     # build multiple confgs
#     auth = 'MD5'
#     priv = 'DES'
#     name = 'instance_{}_{}'.format(auth, priv)
#     config['instances'].append(
#         self.generate_v3_instance_config(
#             self.TABULAR_OBJECTS,
#             name=name,
#             user='datadog{}{}'.format(auth.upper(), priv.upper()),
#             auth=self.AUTH_PROTOCOLS[auth],
#             auth_key=self.AUTH_KEY,
#             priv=self.PRIV_PROTOCOLS[priv],
#             priv_key=self.PRIV_KEY
#         )
#     )
#
#
#     self.run_check_n(config, repeat=3, sleep=2)
#     self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 1, RESULTS_TIMEOUT)
#
#     # Test metrics
#     for symbol in self.TABULAR_OBJECTS[0]['symbols']:
#         metric_name = "snmp." + symbol
#         self.assertMetric(metric_name, at_least=1)
#         self.assertMetricTag(metric_name, self.CHECK_TAGS[0], at_least=1)
#
#         for mtag in self.TABULAR_OBJECTS[0]['metric_tags']:
#             tag = mtag['tag']
#             self.assertMetricTagPrefix(metric_name, tag, at_least=1)
#
#     # Test service check
#     self.assertServiceCheck("snmp.can_check", status=AgentCheck.OK,
#                             tags=self.CHECK_TAGS, at_least=1)
#
#     self.coverage_report()
#
#
# def test_table_v3_MD5_AES(self):
#     """
#     Support SNMP V3 priv modes: MD5 + AES
#     """
#     config = {
#         'instances': []
#     }
#
#     # build multiple confgs
#     auth = 'MD5'
#     priv = 'AES'
#     name = 'instance_{}_{}'.format(auth, priv)
#     config['instances'].append(
#         self.generate_v3_instance_config(
#             self.TABULAR_OBJECTS,
#             name=name,
#             user='datadog{}{}'.format(auth.upper(), priv.upper()),
#             auth=self.AUTH_PROTOCOLS[auth],
#             auth_key=self.AUTH_KEY,
#             priv=self.PRIV_PROTOCOLS[priv],
#             priv_key=self.PRIV_KEY
#         )
#     )
#
#
#     self.run_check_n(config, repeat=3, sleep=2)
#     self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 1, RESULTS_TIMEOUT)
#
#     # Test metrics
#     for symbol in self.TABULAR_OBJECTS[0]['symbols']:
#         metric_name = "snmp." + symbol
#         self.assertMetric(metric_name, at_least=1)
#         self.assertMetricTag(metric_name, self.CHECK_TAGS[0], at_least=1)
#
#         for mtag in self.TABULAR_OBJECTS[0]['metric_tags']:
#             tag = mtag['tag']
#             self.assertMetricTagPrefix(metric_name, tag, at_least=1)
#
#     # Test service check
#     self.assertServiceCheck("snmp.can_check", status=AgentCheck.OK,
#                             tags=self.CHECK_TAGS, at_least=1)
#
#     self.coverage_report()
#
#
# def test_table_v3_SHA_DES(self):
#     """
#     Support SNMP V3 priv modes: SHA + DES
#     """
#     config = {
#         'instances': []
#     }
#
#     # build multiple confgs
#     auth = 'SHA'
#     priv = 'DES'
#     name = 'instance_{}_{}'.format(auth, priv)
#     config['instances'].append(
#         self.generate_v3_instance_config(
#             self.TABULAR_OBJECTS,
#             name=name,
#             user='datadog{}{}'.format(auth.upper(), priv.upper()),
#             auth=self.AUTH_PROTOCOLS[auth],
#             auth_key=self.AUTH_KEY,
#             priv=self.PRIV_PROTOCOLS[priv],
#             priv_key=self.PRIV_KEY
#         )
#     )
#
#
#     self.run_check_n(config, repeat=3, sleep=2)
#     self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 1, RESULTS_TIMEOUT)
#
#     # Test metrics
#     for symbol in self.TABULAR_OBJECTS[0]['symbols']:
#         metric_name = "snmp." + symbol
#         self.assertMetric(metric_name, at_least=1)
#         self.assertMetricTag(metric_name, self.CHECK_TAGS[0], at_least=1)
#
#         for mtag in self.TABULAR_OBJECTS[0]['metric_tags']:
#             tag = mtag['tag']
#             self.assertMetricTagPrefix(metric_name, tag, at_least=1)
#
#     # Test service check
#     self.assertServiceCheck("snmp.can_check", status=AgentCheck.OK,
#                             tags=self.CHECK_TAGS, at_least=1)
#
#     self.coverage_report()
#
#
# def test_table_v3_SHA_AES(self):
#     """
#     Support SNMP V3 priv modes: SHA + AES
#     """
#     config = {
#         'instances': []
#     }
#
#     # build multiple confgs
#     auth = 'SHA'
#     priv = 'AES'
#     name = 'instance_{}_{}'.format(auth, priv)
#     config['instances'].append(
#         self.generate_v3_instance_config(
#             self.TABULAR_OBJECTS,
#             name=name,
#             user='datadog{}{}'.format(auth.upper(), priv.upper()),
#             auth=self.AUTH_PROTOCOLS[auth],
#             auth_key=self.AUTH_KEY,
#             priv=self.PRIV_PROTOCOLS[priv],
#             priv_key=self.PRIV_KEY
#         )
#     )
#
#
#     self.run_check_n(config, repeat=3, sleep=2)
#     self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 1, RESULTS_TIMEOUT)
#
#     # Test metrics
#     for symbol in self.TABULAR_OBJECTS[0]['symbols']:
#         metric_name = "snmp." + symbol
#         self.assertMetric(metric_name, at_least=1)
#         self.assertMetricTag(metric_name, self.CHECK_TAGS[0], at_least=1)
#
#         for mtag in self.TABULAR_OBJECTS[0]['metric_tags']:
#             tag = mtag['tag']
#             self.assertMetricTagPrefix(metric_name, tag, at_least=1)
#
#     # Test service check
#     self.assertServiceCheck("snmp.can_check", status=AgentCheck.OK,
#                             tags=self.CHECK_TAGS, at_least=1)
#
#     self.coverage_report()
#
#
# def test_invalid_metric(self):
#     """
#     Invalid metrics raise a Warning and a critical service check
#     """
#     config = {
#         'instances': [self.generate_instance_config(self.INVALID_METRICS)]
#     }
#     self.run_check(config)
#
#     self.warnings = self.wait_for_async('get_warnings', 'warnings', 1, RESULTS_TIMEOUT)
#     self.assertWarning("Fail to collect some metrics: No symbol IF-MIB::noIdeaWhatIAmDoingHere",
#                        count=1, exact_match=False)
#
#     # # Test service check
#     self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 1, RESULTS_TIMEOUT)
#     self.assertServiceCheck("snmp.can_check", status=AgentCheck.CRITICAL,
#                             tags=self.CHECK_TAGS, count=1)
#     self.coverage_report()
#
#
# def test_forcedtype_metric(self):
#     """
#     Forced Types should be reported as metrics of the forced type
#     """
#     config = {
#         'instances': [self.generate_instance_config(self.FORCED_METRICS)]
#     }
#     self.run_check_twice(config)
#     self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 1, RESULTS_TIMEOUT)
#
#     for metric in self.FORCED_METRICS:
#         metric_name = "snmp." + (metric.get('name') or metric.get('symbol'))
#         if metric.get('forced_type') == MetricTypes.COUNTER:
#             # rate will be flushed as a gauge, so count should be 0.
#             self.assertMetric(metric_name, tags=self.CHECK_TAGS,
#                               count=0, metric_type=MetricTypes.GAUGE)
#         elif metric.get('forced_type') == MetricTypes.GAUGE:
#             self.assertMetric(metric_name, tags=self.CHECK_TAGS,
#                               count=1, metric_type=MetricTypes.GAUGE)
#
#     # # Test service check
#     self.assertServiceCheck("snmp.can_check", status=AgentCheck.OK,
#                             tags=self.CHECK_TAGS, at_least=1)
#     self.coverage_report()
#
#
# def test_invalid_forcedtype_metric(self):
#     """
#     If a forced type is invalid a warning should be issued + a service check
#     should be available
#     """
#     config = {
#         'instances': [self.generate_instance_config(self.INVALID_FORCED_METRICS)]
#     }
#
#     self.run_check(config)
#
#     self.warnings = self.wait_for_async('get_warnings', 'warnings', 1, RESULTS_TIMEOUT)
#     self.assertWarning("Invalid forced-type specified:", count=1, exact_match=False)
#
#     # # Test service check
#     self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 1, RESULTS_TIMEOUT)
#     self.assertServiceCheck("snmp.can_check", status=AgentCheck.CRITICAL,
#                             tags=self.CHECK_TAGS, count=1)
#     self.coverage_report()
#
#
# def test_scalar_with_tags(self):
#     """
#     Support SNMP scalar objects with tags
#     """
#     config = {
#         'instances': [self.generate_instance_config(self.SCALAR_OBJECTS_WITH_TAGS)]
#     }
#     self.run_check_n(config, repeat=3)
#     self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 1, RESULTS_TIMEOUT)
#
#     # Test metrics
#     for metric in self.SCALAR_OBJECTS_WITH_TAGS:
#         metric_name = "snmp." + (metric.get('name') or metric.get('symbol'))
#         tags = self.CHECK_TAGS + metric.get('metric_tags')
#         self.assertMetric(metric_name, tags=tags, count=1)
#     # Test service check
#     self.assertServiceCheck("snmp.can_check", status=AgentCheck.OK, tags=self.CHECK_TAGS, at_least=1)
#
#     self.coverage_report()
#
#
# def test_network_failure(self):
#     """
#     Network failure is reported in service check
#     """
#     instance = self.generate_instance_config(self.SCALAR_OBJECTS)
#
#     # Change port so connection will fail
#     instance['port'] = 162
#
#     config = {
#         'instances': [instance]
#     }
#     self.run_check(config)
#     self.warnings = self.wait_for_async('get_warnings', 'warnings', 1, RESULTS_TIMEOUT)
#
#     self.assertWarning("No SNMP response received before timeout for instance localhost", count=1)
#
#     # Test service check
#     self.service_checks = self.wait_for_async('get_service_checks', 'service_checks', 1, RESULTS_TIMEOUT)
#     self.assertServiceCheck("snmp.can_check", status=AgentCheck.CRITICAL,
#                             tags=self.CHECK_TAGS, count=1)
#
#     self.coverage_report()
