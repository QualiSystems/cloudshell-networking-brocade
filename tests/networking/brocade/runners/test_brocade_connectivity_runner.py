#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.cli.brocade_cli_handler import BrocadeCliHandler
from cloudshell.networking.brocade.flows.brocade_add_vlan_flow import BrocadeAddVlanFlow
from cloudshell.networking.brocade.flows.brocade_remove_vlan_flow import BrocadeRemoveVlanFlow
from cloudshell.networking.brocade.runners.brocade_connectivity_runner import BrocadeConnectivityRunner


class TestBrocadeConnectivityRunner(unittest.TestCase):
    def setUp(self):
        cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        resource_config = mock.MagicMock()
        api = mock.MagicMock()
        super(TestBrocadeConnectivityRunner, self).setUp()
        self.tested_instance = BrocadeConnectivityRunner(cli=cli_handler,
                                                         logger=logger,
                                                         resource_config=resource_config,
                                                         api=api)

    def tearDown(self):
        super(TestBrocadeConnectivityRunner, self).tearDown()
        del self.tested_instance

    def test_cli_handler_property(self):
        """ Check that property return correct instance. Should return BrocadeCliHandler """

        self.assertIsInstance(self.tested_instance.cli_handler, BrocadeCliHandler)

    def test_add_vlan_flow_property(self):
        """ Check that property return correct instance. Should return BrocadeAddVlanFlow """

        self.assertIsInstance(self.tested_instance.add_vlan_flow, BrocadeAddVlanFlow)

    def test_remove_vlan_flow_property(self):
        """ Check that property return correct instance. Should return BrocadeRemoveVlanFlow """

        self.assertIsInstance(self.tested_instance.remove_vlan_flow, BrocadeRemoveVlanFlow)
