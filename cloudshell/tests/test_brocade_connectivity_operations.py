#!/usr/bin/python
# -*- coding: utf-8 -*-

from mock import MagicMock as Mock
from unittest import TestCase

from cloudshell.networking.brocade.brocade_connectivity_operations import BrocadeConnectivityOperations


class TestBrocadeConnectivityOperations(TestCase):
    def setUp(self):
        self._context = Mock()
        self._api = Mock()
        self._cli_service = Mock()
        self._logger = Mock()
        self._connectivity_operations_instance = BrocadeConnectivityOperations(context=self._context,
                                                                               api=self._api,
                                                                               cli_service=self._cli_service,
                                                                               logger=self._logger)

    def test_validate_vlan_methods_incoming_parameters(self):
        pass

    def test_get_vlan_list_success(self):
        self.assertEqual(self._connectivity_operations_instance._get_vlan_list("2, 3, 5-8, 7"), [2, 3, 5, 6, 7, 8])

    def test_get_vlan_list_exception_1(self):
        self.assertRaises(self._connectivity_operations_instance._get_vlan_list("2, 3, 5000"), Exception)

    def test_get_vlan_list_exception_2(self):
        self.assertEqual(self._connectivity_operations_instance._get_vlan_list("2, 4000-5000"), Exception)

    def test_get_resource_full_name(self):
        pass

    def test_get_port_name(self):
        pass

    def test_does_interface_support_qnq_False(self):
        self._cli_service.send_config_command = Mock(side_effect=["", "Unrecognized command"])
        self.assertTrue(self._connectivity_operations_instance._does_interface_support_qnq("ethernet 2/1"))

    def test_does_interface_support_qnq_True(self):
        self._cli_service.send_config_command = Mock(side_effect=["", "enable "])
        self.assertTrue(self._connectivity_operations_instance._does_interface_support_qnq("ethernet 2/1"))
