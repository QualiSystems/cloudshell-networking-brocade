#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.runners.configuration_runner import ConfigurationRunner
from cloudshell.networking.brocade.cli.brocade_cli_handler import BrocadeCliHandler
from cloudshell.networking.brocade.flows.brocade_restore_flow import BrocadeRestoreFlow
from cloudshell.networking.brocade.flows.brocade_save_flow import BrocadeSaveFlow


class BrocadeConfigurationRunner(ConfigurationRunner):
    def __init__(self, cli, logger, resource_config, api):
        super(BrocadeConfigurationRunner, self).__init__(logger, resource_config, api)
        self._cli = cli

    @property
    def cli_handler(self):
        """ CLI Handler property
        :return: CLI handler
        """
        return BrocadeCliHandler(self._cli, self.resource_config, self._logger, self._api)

    @property
    def restore_flow(self):
        return BrocadeRestoreFlow(cli_handler=self.cli_handler, logger=self._logger)

    @property
    def save_flow(self):
        return BrocadeSaveFlow(cli_handler=self.cli_handler, logger=self._logger)

    @property
    def file_system(self):
        return ""
