#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.flows.brocade_disable_snmp_flow import BrocadeDisableSnmpFlow
from cloudshell.snmp.snmp_parameters import SNMPV2ReadParameters


class TestDisableSnmpFlow(unittest.TestCase):
    def setUp(self):
        cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        super(TestDisableSnmpFlow, self).setUp()
        self.tested_instance = BrocadeDisableSnmpFlow(cli_handler=cli_handler, logger=logger)

    def tearDown(self):
        super(TestDisableSnmpFlow, self).tearDown()
        del self.tested_instance

    @mock.patch("cloudshell.networking.brocade.flows.brocade_disable_snmp_flow.EnableDisableSnmpActions")
    def test_execute_flow_success(self, snmp_actions_class):
        """ SNMP Community already configured """

        test_snmp_community = "snmp_community"

        snmp_parameters = SNMPV2ReadParameters(ip="127.0.0.1", snmp_read_community=test_snmp_community)
        snmp_actions = mock.MagicMock()
        snmp_actions_class.return_value = snmp_actions

        self.tested_instance.execute_flow(snmp_parameters)
        snmp_actions.disable_snmp_community.assert_called_once_with(test_snmp_community)
        snmp_actions.disable_snmp_server.assert_called_once()

    @mock.patch("cloudshell.networking.brocade.flows.brocade_disable_snmp_flow.EnableDisableSnmpActions")
    def test_execute_flow_skip_unsupported_version(self, snmp_actions_class):
        """ Disable SNMP Read Community skipped. Unsupported SNMP Version """

        snmp_parameters = "Some SNMP Parameters structure"
        snmp_actions = mock.MagicMock()
        snmp_actions_class.return_value = snmp_actions

        self.tested_instance.execute_flow(snmp_parameters)
        snmp_actions.disable_snmp_community.assert_not_called()
        snmp_actions.disable_snmp_server.assert_not_called()

    @mock.patch("cloudshell.networking.brocade.flows.brocade_disable_snmp_flow.EnableDisableSnmpActions")
    def test_execute_flow_skip_empty_community(self, snmp_actions_class):
        """ Disable SNMP Read Community skipped. SNMP Read Community is Empty """

        snmp_parameters = SNMPV2ReadParameters(ip="127.0.0.1", snmp_read_community="")
        snmp_actions = mock.MagicMock()
        snmp_actions_class.return_value = snmp_actions

        self.tested_instance.execute_flow(snmp_parameters)
        snmp_actions.disable_snmp_community.assert_not_called()
        snmp_actions.disable_snmp_server.assert_not_called()
