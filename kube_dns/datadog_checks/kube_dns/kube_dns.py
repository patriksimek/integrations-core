# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from datadog_checks.checks.openmetrics import OpenMetricsBaseCheck


class KubeDNSCheck(OpenMetricsBaseCheck):
    """
    Collect kube-dns metrics from Prometheus
    """

    # Set up metric_transformers
    METRIC_TRANSFORMERS = {}

    def __init__(self, name, init_config, agentConfig, instances=None):
        # Set up metric_transformers
        self.METRIC_TRANSFORMERS = {
            'kubedns_kubedns_dns_request_count_total': self.kubedns_kubedns_dns_request_count_total,
            'kubedns_kubedns_dns_error_count_total': self.kubedns_kubedns_dns_error_count_total,
            'kubedns_kubedns_dns_cachemiss_count_total': self.kubedns_kubedns_dns_cachemiss_count_total,
            'skydns_skydns_dns_request_count_total': self.skydns_skydns_dns_request_count_total,
            'skydns_skydns_dns_error_count_total': self.skydns_skydns_dns_error_count_total,
            'skydns_skydns_dns_cachemiss_count_total': self.skydns_skydns_dns_cachemiss_count_total
        }

        # Create instances we can use in OpenMetricsBaseCheck
        generic_instances = None
        if instances is not None:
            generic_instances = self.create_generic_instances(instances)

        super(KubeDNSCheck, self).__init__(name, init_config, agentConfig, instances=generic_instances)

    def check(self, instance):
        endpoint = instance.get('prometheus_endpoint')
        scraper_config = self.config_map[endpoint]
        self.process(scraper_config, metric_transformers=self.METRIC_TRANSFORMERS)

    def create_generic_instances(self, instances):
        """
        Transform each Kube DNS instance into a OpenMetricsBaseCheck instance
        """
        generic_instances = []
        for instance in instances:
            transformed_instance = self._create_kube_dns_instance(instance)
            generic_instances.append(transformed_instance)

        return generic_instances

    def _create_kube_dns_instance(self, instance):
        """
        Set up kube_dns instance so it can be used in OpenMetricsBaseCheck
        """
        # kube_dns uses 'prometheus_endpoint' and not 'prometheus_url', so we have to rename the key
        instance['prometheus_url'] = instance.get('prometheus_endpoint', None)

        instance.update({
            'namespace': 'kubedns',

            # Note: the count metrics were moved to specific functions list below to be submitted
            # as both gauges and monotonic_counts
            'metrics': [{
                # metrics have been renamed to kubedns in kubernetes 1.6.0
                'kubedns_kubedns_dns_response_size_bytes': 'response_size.bytes',
                'kubedns_kubedns_dns_request_duration_seconds': 'request_duration.seconds',
                # metrics names for kubernetes < 1.6.0
                'skydns_skydns_dns_response_size_bytes': 'response_size.bytes',
                'skydns_skydns_dns_request_duration_seconds': 'request_duration.seconds',
            }]
        })

        return instance

    def submit_as_gauge_and_monotonic_count(self, metric_suffix, message, scraper_config):
        """
        submit a kube_dns metric both as a gauge (for compatibility) and as a monotonic_count
        """
        metric_name = scraper_config['namespace'] + metric_suffix
        for metric in message.metric:
            _tags = []
            for label in metric.label:
                _tags.append('{}:{}'.format(label.name, label.value))
            # submit raw metric
            self.gauge(metric_name, metric.counter.value, _tags)
            # submit rate metric
            self.monotonic_count(metric_name + '.count', metric.counter.value, _tags)

    # metrics names for kubernetes >= 1.6.0
    def kubedns_kubedns_dns_request_count_total(self, message, scraper_config):
        self.submit_as_gauge_and_monotonic_count('.request_count', message, scraper_config)

    def kubedns_kubedns_dns_error_count_total(self, message, scraper_config):
        self.submit_as_gauge_and_monotonic_count('.error_count', message, scraper_config)

    def kubedns_kubedns_dns_cachemiss_count_total(self, message, scraper_config):
        self.submit_as_gauge_and_monotonic_count('.cachemiss_count', message, scraper_config)

    # metrics names for kubernetes < 1.6.0
    def skydns_skydns_dns_request_count_total(self, message, scraper_config):
        self.kubedns_kubedns_dns_request_count_total(message, scraper_config)

    def skydns_skydns_dns_error_count_total(self, message, scraper_config):
        self.kubedns_kubedns_dns_error_count_total(message, scraper_config)

    def skydns_skydns_dns_cachemiss_count_total(self, message, scraper_config):
        self.kubedns_kubedns_dns_cachemiss_count_total(message, scraper_config)
