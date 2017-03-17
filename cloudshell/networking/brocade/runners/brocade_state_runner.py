#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.runners.state_runner import StateRunner
from cloudshell.networking.brocade.cli.brocade_cli_handler import BrocadeCliHandler


class BrocadeStateRunner(StateRunner):
    def __init__(self, cli, logger, api, resource_config):
        """

        :param cli:
        :param logger:
        :param api:
        :param resource_config:
        """

        super(BrocadeStateRunner, self).__init__(logger, api, resource_config)
        self.cli = cli
        self.api = api

    @property
    def cli_handler(self):
        return BrocadeCliHandler(self.cli, self.resource_config, self._logger, self.api)
