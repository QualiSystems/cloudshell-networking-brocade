#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.flows.brocade_autoload_flow import BrocadeSnmpAutoloadFlow
from cloudshell.networking.brocade.snmp.brocade_snmp_handler import BrocadeSnmpHandler
from cloudshell.networking.brocade.runners.brocade_autoload_runner import BrocadeAutoloadRunner


class TestBrocadeAutoloadRunner(unittest.TestCase):
    def setUp(self):
        cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        resource_config = mock.MagicMock()
        api = mock.MagicMock()
        super(TestBrocadeAutoloadRunner, self).setUp()
        self.tested_instance = BrocadeAutoloadRunner(cli=cli_handler,
                                                     logger=logger,
                                                     resource_config=resource_config,
                                                     api=api)

    def tearDown(self):
        super(TestBrocadeAutoloadRunner, self).tearDown()
        del self.tested_instance

    def test_snmp_handler_property(self):
        """ Check that property return correct instance. Should return BrocadeSnmpHandler """

        self.assertIsInstance(self.tested_instance.snmp_handler, BrocadeSnmpHandler)

    def test_autoload_flow_property(self):
        """ Check that property return correct instance. Should return BrocadeSnmpAutoloadFlow """

        self.assertIsInstance(self.tested_instance.autoload_flow, BrocadeSnmpAutoloadFlow)
