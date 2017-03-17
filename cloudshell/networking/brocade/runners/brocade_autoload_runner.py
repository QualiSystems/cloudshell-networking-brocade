#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.runners.autoload_runner import AutoloadRunner

from cloudshell.networking.brocade.flows.brocade_autoload_flow import BrocadeSnmpAutoloadFlow
from cloudshell.networking.brocade.snmp.brocade_snmp_handler import BrocadeSnmpHandler


class BrocadeAutoloadRunner(AutoloadRunner):
    def __init__(self, cli, logger, resource_config, api):
        super(BrocadeAutoloadRunner, self).__init__(resource_config)
        self._cli = cli
        self._api = api
        self._logger = logger

    @property
    def snmp_handler(self):
        return BrocadeSnmpHandler(self._cli, self.resource_config, self._logger, self._api)

    @property
    def autoload_flow(self):
        return BrocadeSnmpAutoloadFlow(self.snmp_handler, self._logger)
