#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.cli.brocade_cli_handler import BrocadeCliHandler
from cloudshell.networking.brocade.flows.brocade_load_firmware_flow import BrocadeLoadFirmwareFlow
from cloudshell.networking.brocade.runners.brocade_firmware_runner import BrocadeFirmwareRunner


class TestBrocadeFirmwareRunner(unittest.TestCase):
    def setUp(self):
        cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        resource_config = mock.MagicMock()
        api = mock.MagicMock()
        super(TestBrocadeFirmwareRunner, self).setUp()
        self.tested_instance = BrocadeFirmwareRunner(cli=cli_handler,
                                                     logger=logger,
                                                     resource_config=resource_config,
                                                     api=api)

    def tearDown(self):
        super(TestBrocadeFirmwareRunner, self).tearDown()
        del self.tested_instance

    def test_cli_handler_property(self):
        """ Check that property return correct instance. Should return BrocadeCliHandler """

        self.assertIsInstance(self.tested_instance.cli_handler, BrocadeCliHandler)

    def test_load_firmware_flow_property(self):
        """ Check that property return correct instance. Should return BrocadeLoadFirmwareFlow """

        self.assertIsInstance(self.tested_instance.load_firmware_flow, BrocadeLoadFirmwareFlow)
