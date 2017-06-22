#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.cli.brocade_cli_handler import BrocadeCliHandler
from cloudshell.networking.brocade.flows.brocade_restore_flow import BrocadeRestoreFlow
from cloudshell.networking.brocade.flows.brocade_save_flow import BrocadeSaveFlow
from cloudshell.networking.brocade.runners.brocade_configuration_runner import BrocadeConfigurationRunner


class TestBrocadeConfigurationRunner(unittest.TestCase):
    def setUp(self):
        cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        resource_config = mock.MagicMock()
        api = mock.MagicMock()
        super(TestBrocadeConfigurationRunner, self).setUp()
        self.tested_instance = BrocadeConfigurationRunner(cli=cli_handler,
                                                          logger=logger,
                                                          resource_config=resource_config,
                                                          api=api)

    def tearDown(self):
        super(TestBrocadeConfigurationRunner, self).tearDown()
        del self.tested_instance

    def test_cli_handler_property(self):
        """ Check that property return correct instance. Should return BrocadeCliHandler """

        self.assertIsInstance(self.tested_instance.cli_handler, BrocadeCliHandler)

    def test_restore_flow_property(self):
        """ Check that property return correct instance. Should return BrocadeRestoreFlow """

        self.assertIsInstance(self.tested_instance.restore_flow, BrocadeRestoreFlow)

    def test_save_flow_property(self):
        """ Check that property return correct instance. Should return BrocadeSaveFlow """

        self.assertIsInstance(self.tested_instance.save_flow, BrocadeSaveFlow)

    def test_file_system_property(self):
        """ Check that property return correct instance. Should return empty string """

        self.assertEqual(self.tested_instance.file_system, "")
