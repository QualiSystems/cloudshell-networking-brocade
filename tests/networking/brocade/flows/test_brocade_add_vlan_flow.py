#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.flows.brocade_add_vlan_flow import BrocadeAddVlanFlow


class TestBrocadeAddVlanFlow(unittest.TestCase):
    def setUp(self):
        cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        super(TestBrocadeAddVlanFlow, self).setUp()
        self.tested_instance = BrocadeAddVlanFlow(cli_handler=cli_handler, logger=logger)

    def tearDown(self):
        super(TestBrocadeAddVlanFlow, self).tearDown()
        del self.tested_instance

    def test_execute_flow_fail_unsupported_port_mode(self):
        """ Unsupported port mode """

        with self.assertRaisesRegexp(Exception, "Unsupported port mode"):
            self.tested_instance.execute_flow("vlan_range", "port_mode", "port_name", False, "c_tag")

    @mock.patch("cloudshell.networking.brocade.flows.brocade_add_vlan_flow.AddRemoveVlanActions")
    @mock.patch("cloudshell.networking.brocade.flows.brocade_add_vlan_flow.IFaceActions")
    def test_execute_flow_success_without_qnq(self, if_actions_class, vlan_actions_class):
        """ Successfully create VLAN without QnQ """

        if_actions = mock.MagicMock()
        if_actions_class.return_value = if_actions
        if_actions.get_port_name.return_value = "port_name"
        vlan_actions = mock.MagicMock()
        vlan_actions_class.return_value = vlan_actions

        self.tested_instance.execute_flow("10", "trunk", "full_port_name", False, "c_tag")

        if_actions.get_port_name.assert_called_once_with("full_port_name")
        vlan_actions.configure_vlan.assert_called_once_with("10")
        vlan_actions.set_vlan_to_interface.assert_called_once_with(tag_type="tagged", port_name="port_name")
        if_actions.does_interface_support_qnq.assert_not_called()
        if_actions.enable_qnq.assert_not_called()

    @mock.patch("cloudshell.networking.brocade.flows.brocade_add_vlan_flow.AddRemoveVlanActions")
    @mock.patch("cloudshell.networking.brocade.flows.brocade_add_vlan_flow.IFaceActions")
    def test_execute_flow_success_with_qnq(self, if_actions_class, vlan_actions_class):
        """ Successfully create VLAN with QnQ. QnQ isn't supported """

        if_actions = mock.MagicMock()
        if_actions_class.return_value = if_actions
        if_actions.get_port_name.return_value = "port_name"
        if_actions.does_interface_support_qnq.return_value = False

        vlan_actions = mock.MagicMock()
        vlan_actions_class.return_value = vlan_actions

        self.tested_instance.execute_flow("10", "trunk", "full_port_name", True, "c_tag")

        if_actions.get_port_name.assert_called_once_with("full_port_name")
        vlan_actions.configure_vlan.assert_called_once_with("10")
        vlan_actions.set_vlan_to_interface.assert_called_once_with(tag_type="tagged", port_name="port_name")
        if_actions.does_interface_support_qnq.assert_called_once_with(port_name="port_name")
        if_actions.enable_qnq.assert_not_called()

    @mock.patch("cloudshell.networking.brocade.flows.brocade_add_vlan_flow.AddRemoveVlanActions")
    @mock.patch("cloudshell.networking.brocade.flows.brocade_add_vlan_flow.IFaceActions")
    def test_execute_flow_success_with_qnq(self, if_actions_class, vlan_actions_class):
        """ Successfully create VLAN with QnQ """

        if_actions = mock.MagicMock()
        if_actions_class.return_value = if_actions
        if_actions.get_port_name.return_value = "port_name"
        if_actions.does_interface_support_qnq.return_value = True

        vlan_actions = mock.MagicMock()
        vlan_actions_class.return_value = vlan_actions

        self.tested_instance.execute_flow("10", "trunk", "full_port_name", True, "c_tag")

        if_actions.get_port_name.assert_called_once_with("full_port_name")
        vlan_actions.configure_vlan.assert_called_once_with("10")
        vlan_actions.set_vlan_to_interface.assert_called_once_with(tag_type="tagged", port_name="port_name")
        if_actions.does_interface_support_qnq.assert_called_once_with(port_name="port_name")
        if_actions.enable_qnq.assert_called_once_with(port_name="port_name")

    @mock.patch("cloudshell.networking.brocade.flows.brocade_add_vlan_flow.AddRemoveVlanActions")
    @mock.patch("cloudshell.networking.brocade.flows.brocade_add_vlan_flow.IFaceActions")
    def test_execute_flow_fail(self, if_actions_class, vlan_actions_class):
        """ Failed create VLAN """

        if_actions = mock.MagicMock()
        if_actions_class.return_value = if_actions
        if_actions.get_port_name.return_value = "port_name"

        vlan_actions = mock.MagicMock()
        vlan_actions_class.return_value = vlan_actions
        vlan_actions.configure_vlan = mock.MagicMock(side_effect=[Exception])

        with self.assertRaisesRegexp(Exception, "\[FAIL\] VLAN\(s\) 10 configuration failed"):
            self.tested_instance.execute_flow("10", "trunk", "full_port_name", True, "c_tag")
