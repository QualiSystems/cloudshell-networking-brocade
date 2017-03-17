#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.networking.brocade.cli.brocade_cli_handler import BrocadeCliHandler
from cloudshell.networking.brocade.flows.brocade_disable_snmp_flow import BrocadeDisableSnmpFlow
from cloudshell.networking.brocade.flows.brocade_enable_snmp_flow import BrocadeEnableSnmpFlow
from cloudshell.devices.snmp_handler import SnmpHandler


class BrocadeSnmpHandler(SnmpHandler):
    def __init__(self, cli, resource_config, logger, api):
        super(BrocadeSnmpHandler, self).__init__(resource_config, logger, api)
        self._cli = cli
        self._api = api

    @property
    def cli_handler(self):
        return BrocadeCliHandler(self._cli, self.resource_config, self._logger, self._api)

    def _create_enable_flow(self):
        return BrocadeEnableSnmpFlow(self.cli_handler, self._logger)

    def _create_disable_flow(self):
        return BrocadeDisableSnmpFlow(self.cli_handler, self._logger)
