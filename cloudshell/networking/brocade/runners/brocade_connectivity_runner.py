#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.runners.connectivity_runner import ConnectivityRunner
from cloudshell.networking.brocade.cli.brocade_cli_handler import BrocadeCliHandler
from cloudshell.networking.brocade.flows.brocade_add_vlan_flow import BrocadeAddVlanFlow
from cloudshell.networking.brocade.flows.brocade_remove_vlan_flow import BrocadeRemoveVlanFlow


class BrocadeConnectivityRunner(ConnectivityRunner):
    IS_VLAN_RANGE_SUPPORTED = False

    def __init__(self, cli, logger, api, resource_config):
        """ Handle add/remove vlan flows

            :param cli:
            :param logger:
            :param api:
            :param resource_config:
            """

        super(BrocadeConnectivityRunner, self).__init__(logger)
        self.cli = cli
        self.api = api
        self.resource_config = resource_config

    @property
    def cli_handler(self):
        return BrocadeCliHandler(self.cli, self.resource_config, self._logger, self.api)

    @property
    def add_vlan_flow(self):
        return BrocadeAddVlanFlow(self.cli_handler, self._logger)

    @property
    def remove_vlan_flow(self):
        return BrocadeRemoveVlanFlow(self.cli_handler, self._logger)
