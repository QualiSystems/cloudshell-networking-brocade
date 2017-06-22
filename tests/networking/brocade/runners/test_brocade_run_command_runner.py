#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.cli.brocade_cli_handler import BrocadeCliHandler
from cloudshell.networking.brocade.runners.brocade_run_command_runner import BrocadeRunCommandRunner


class TestBrocadeRunCommandRunner(unittest.TestCase):
    def setUp(self):
        cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        resource_config = mock.MagicMock()
        api = mock.MagicMock()
        super(TestBrocadeRunCommandRunner, self).setUp()
        self.tested_instance = BrocadeRunCommandRunner(cli=cli_handler,
                                                       logger=logger,
                                                       resource_config=resource_config,
                                                       api=api)

    def tearDown(self):
        super(TestBrocadeRunCommandRunner, self).tearDown()
        del self.tested_instance

    def test_cli_handler_property(self):
        """ Check that property return correct instance. Should return BrocadeCliHandler """

        self.assertIsInstance(self.tested_instance.cli_handler, BrocadeCliHandler)
