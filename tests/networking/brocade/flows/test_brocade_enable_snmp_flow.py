#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.flows.brocade_enable_snmp_flow import BrocadeEnableSnmpFlow
from cloudshell.snmp.snmp_parameters import SNMPV2ReadParameters


class TestBrocadeEnableSnmpFlow(unittest.TestCase):
    def setUp(self):
        cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        super(TestBrocadeEnableSnmpFlow, self).setUp()
        self.tested_instance = BrocadeEnableSnmpFlow(cli_handler=cli_handler, logger=logger)

    def tearDown(self):
        super(TestBrocadeEnableSnmpFlow, self).tearDown()
        del self.tested_instance

    def test_execute_flow_fail_unsupported_version(self):
        """ Unsupported SNMP Version """

        snmp_parameters = "Some SNMP Parameters structure"

        with self.assertRaisesRegexp(Exception, "Unsupported SNMP version"):
            self.tested_instance.execute_flow(snmp_parameters)

    def test_execute_flow_fail_empty_snmp_community(self):
        """ SNMP Community should not be empty """

        snmp_parameters = SNMPV2ReadParameters(ip="127.0.0.1", snmp_read_community="")

        with self.assertRaisesRegexp(Exception, "SNMP community cannot be empty"):
            self.tested_instance.execute_flow(snmp_parameters)

    @mock.patch("cloudshell.networking.brocade.flows.brocade_enable_snmp_flow.EnableDisableSnmpActions")
    def test_execute_flow_success_already_enabled_and_configured(self, snmp_actions_class):
        """ SNMP Server Enabled and SNMP Read Community already configured """

        test_snmp_community = "read_community"

        snmp_parameters = SNMPV2ReadParameters(ip="127.0.0.1", snmp_read_community=test_snmp_community)
        snmp_actions = mock.MagicMock()
        snmp_actions_class.return_value = snmp_actions
        snmp_actions.get_current_snmp_info.return_value = """ Status: Enabled
                                                              Contact:
                                                              Location:
                                                              Community(ro): read_community
                                                              Community(rw): write_community

                                                              Max Ifindex per module: 64
                                                          """

        self.tested_instance.execute_flow(snmp_parameters)
        snmp_actions.get_current_snmp_info.assert_called_once()
        snmp_actions.enable_snmp_server.assert_not_called()
        snmp_actions.enable_snmp_community.assert_not_called()

    @mock.patch("cloudshell.networking.brocade.flows.brocade_enable_snmp_flow.EnableDisableSnmpActions")
    def test_execute_flow_success_already_enabled(self, snmp_actions_class):
        """ SNMP Server Enabled but SNMP Read Community not configured yet """

        test_snmp_community = "new_read_community"

        snmp_parameters = SNMPV2ReadParameters(ip="127.0.0.1", snmp_read_community=test_snmp_community)
        snmp_actions = mock.MagicMock()
        snmp_actions_class.return_value = snmp_actions
        snmp_actions.get_current_snmp_info.return_value = """ Status: Enabled
                                                              Contact:
                                                              Location:
                                                              Community(ro): read_community
                                                              Community(rw): write_community

                                                              Max Ifindex per module: 64
                                                          """

        self.tested_instance.execute_flow(snmp_parameters)
        snmp_actions.get_current_snmp_info.assert_called_once()
        snmp_actions.enable_snmp_server.assert_not_called()
        snmp_actions.enable_snmp_community.assert_called_once_with(snmp_read_community=test_snmp_community)

    @mock.patch("cloudshell.networking.brocade.flows.brocade_enable_snmp_flow.EnableDisableSnmpActions")
    def test_execute_flow_success(self, snmp_actions_class):
        """ SNMP Server and SNMP Read Community should be configured """

        test_snmp_community = "new_read_community"

        snmp_parameters = SNMPV2ReadParameters(ip="127.0.0.1", snmp_read_community=test_snmp_community)
        snmp_actions = mock.MagicMock()
        snmp_actions_class.return_value = snmp_actions
        snmp_actions.get_current_snmp_info.return_value = """ Status: Disabled
                                                              Contact:
                                                              Location:
                                                              Community(ro): read_community
                                                              Community(rw): write_community

                                                              Max Ifindex per module: 64
                                                          """

        self.tested_instance.execute_flow(snmp_parameters)
        snmp_actions.get_current_snmp_info.assert_called_once()
        snmp_actions.enable_snmp_server.assert_called_once()
        snmp_actions.enable_snmp_community.assert_called_once_with(snmp_read_community=test_snmp_community)
