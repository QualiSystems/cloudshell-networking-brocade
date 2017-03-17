#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.runners.run_command_runner import RunCommandRunner
from cloudshell.networking.brocade.cli.brocade_cli_handler import BrocadeCliHandler


class BrocadeRunCommandRunner(RunCommandRunner):
    def __init__(self, cli, resource_config, logger, api):
        """Create BrocadeRunCommandOperations

        :param context: command context
        :param api: cloudshell api object
        :param cli: CLI object
        :param logger: QsLogger object
        :return:
        """

        super(BrocadeRunCommandRunner, self).__init__(logger)
        self.cli = cli
        self.api = api
        self.resource_config = resource_config

    @property
    def cli_handler(self):
        return BrocadeCliHandler(self.cli, self.resource_config, self._logger, self.api)
