#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.autoload.brocade_generic_snmp_autoload import BrocadeGenericSNMPAutoload


class TestBrocadeGenericSNMPAutoload(unittest.TestCase):
    def setUp(self):
        self.snmp_handler = mock.MagicMock()
        logger = mock.MagicMock()
        shell_name = "TestShellName"
        shell_type = "CS_Switch"
        resource_name = "Test Brocade Resource"
        self.supported_os = [r"Brocade Operation System"]
        super(TestBrocadeGenericSNMPAutoload, self).setUp()
        self.tested_instance = BrocadeGenericSNMPAutoload(snmp_handler=self.snmp_handler,
                                                          shell_name=shell_name,
                                                          shell_type=shell_type,
                                                          resource_name=resource_name,
                                                          logger=logger)

    def tearDown(self):
        super(TestBrocadeGenericSNMPAutoload, self).tearDown()
        del self.tested_instance

    @mock.patch("cloudshell.networking.brocade.autoload.brocade_generic_snmp_autoload.os")
    def test_load_additional_mibs(self, os_class):
        """  Successfully load additional MIBs """

        path = "some/test/path"
        os_class.path.abspath.return_value = path

        self.tested_instance.load_additional_mibs()
        self.snmp_handler.update_mib_sources.assert_called_once_with(path)

    def test_discover_fail_wrong_device_os(self):
        """ Unsupported device OS determined """

        self.tested_instance._is_valid_device_os = mock.MagicMock(return_value=False)

        with self.assertRaisesRegexp(Exception, "Unsupported device OS"):
            self.tested_instance.discover(self.supported_os)

    def test_is_valid_device_os_true(self):
        """ Successfully check device Operation System """

        self.snmp_handler.get_property.return_value = "Brocade Operation System"
        self.assertTrue(self.tested_instance._is_valid_device_os(self.supported_os))

    def test_is_valid_device_os_false(self):
        """ Failed during check device Operation System """

        self.snmp_handler.get_property.return_value = "Some Device System Description"
        self.assertFalse(self.tested_instance._is_valid_device_os(self.supported_os))

    def test__get_device_model_success(self):
        """ Successfully determine device model """

        device_model = "DEVICE_MODEL"
        self.snmp_handler.get_property.return_value = "qwerty::{}".format(device_model)
        self.assertEqual(self.tested_instance._get_device_model(), device_model.capitalize())

    def test__get_device_model_fail(self):
        """ Failed to determine device model. Return empty string """

        self.snmp_handler.get_property.return_value = "some response"
        self.assertEqual(self.tested_instance._get_device_model(), "")

    def test__get_device_os_version_success(self):
        """ Successfully determine device OS Version """

        device_os_version = "V5.9.0T163"
        self.snmp_handler.get_property.return_value = "Some system device description including Version {}, " \
                                                      "Vendor etc".format(device_os_version)
        self.assertEqual(self.tested_instance._get_device_os_version(), device_os_version)

    def test__get_device_os_version_fail(self):
        """ Failed to determine device OS Version. Return empty string """

        self.snmp_handler.get_property.return_value = "Some system incorrect device description"
        self.assertEqual(self.tested_instance._get_device_os_version(), "")

    def test__get_device_details(self):
        """ Successfully build device root """

        self.snmp_handler.get_property.side_effect = ["contact_name", "system_name", "location"]
        self.tested_instance._get_device_os_version = mock.MagicMock(return_value="os_version")
        self.tested_instance._get_device_model = mock.MagicMock(return_value="device_model")

        self.tested_instance._get_device_details()

        self.assertEquals(self.tested_instance.resource.contact_name, "contact_name")
        self.assertEquals(self.tested_instance.resource.system_name, "system_name")
        self.assertEquals(self.tested_instance.resource.location, "location")
        self.assertEquals(self.tested_instance.resource.os_version, "os_version")
        self.assertEquals(self.tested_instance.resource.model, "device_model")
        self.assertEquals(self.tested_instance.resource.vendor, "Brocade")

    def test__load_snmp_tables_success(self):
        """ Successfully load SNMP Tables """

        self.tested_instance._get_entity_table = mock.MagicMock(return_value={"Some data": "from Entity Table"})

        self.tested_instance._load_snmp_tables()
        self.assertEqual(self.snmp_handler.get_table.call_count, 7)

    def test__load_snmp_tables_fail(self):
        """ Failed during read information from Entity Table """

        self.tested_instance._get_entity_table = mock.MagicMock(return_value={})

        with self.assertRaisesRegexp(Exception, "Cannot load entPhysicalTable"):
            self.tested_instance._load_snmp_tables()
        self.assertEqual(self.snmp_handler.get_table.call_count, 1)

    def test__get_entity_table(self):
        """  """

        pass

    def test__filter_lower_bay_containers(self):
        """  """

        pass

    def test__add_relative_addresss(self):
        """  """

        pass

    def test__get_port_relative_address(self):
        """  """

        pass

    def test__add_element(self):
        """  """

        pass

    def test__get_module_list(self):
        """  """

        pass

    def test__get_module_parents(self):
        """  """

        pass

    def test__get_resource_id(self):
        """  """

        pass

    def test__get_chassis_attributes(self):
        """  """

        pass

    def test__get_module_attributes(self):
        """  """

        pass

    def test__filter_power_port_list(self):
        """  """

        pass

    def test__get_power_supply_parent_id(self):
        """  """

        pass

    def test__get_power_ports(self):
        """  """

        pass

    def test__get_port_channels(self):
        """  """

        pass

    def test__get_associated_ports(self):
        """  """

        pass

    def test__get_ports_attributes(self):
        """  """

        pass

    def test_get_relative_address(self):
        """  """

        pass

    def test__filter_entity_table(self):
        """  """

        pass

    def test__get_ipv4_interface_address_success(self):
        """ Successfully return ipv4 address """

        port_index = 2
        self.tested_instance.ip_v4_table = {"ipv4_address_1": {"ipAdEntIfIndex": "1"},
                                            "ipv4_address_2": {"ipAdEntIfIndex": "2"}}

        self.assertEqual(self.tested_instance._get_ipv4_interface_address(port_index), "ipv4_address_2")

    def test__get_ipv4_interface_address_fail(self):
        """ Failed to determine ipv4 address. Return None """

        port_index = 3
        self.tested_instance.ip_v4_table = {"ipv4_address_1": {"ipAdEntIfIndex": "1"},
                                            "ipv4_address_2": {"ipAdEntIfIndex": "2"}}

        self.assertEqual(self.tested_instance._get_ipv4_interface_address(port_index), None)

    def test__get_ipv6_interface_address_success(self):
        """ Successfully return IPv6 address """

        port_index = 2
        self.tested_instance.ip_v6_table = {"ipv6_address_1": {"ipAdEntIfIndex": "1"},
                                            "ipv6_address_2": {"ipAdEntIfIndex": "2"}}

        self.assertEqual(self.tested_instance._get_ipv6_interface_address(port_index), "ipv6_address_2")

    def test__get_ipv6_interface_address_fail(self):
        """ Failed to determine IPv6 address. Return None """

        port_index = 3
        self.tested_instance.ip_v6_table = {"ipv6_address_1": {"ipAdEntIfIndex": "1"},
                                            "ipv6_address_2": {"ipAdEntIfIndex": "2"}}

        self.assertEqual(self.tested_instance._get_ipv6_interface_address(port_index), None)

    def test__get_port_duplex_full(self):
        """ Successfully determined duplex mode. Return Full """

        self.tested_instance.duplex_table = {"index": {"dot3StatsIndex": "port_index"}}
        self.snmp_handler.get_property.return_value = "fullDuplex"

        self.assertEqual(self.tested_instance._get_port_duplex("port_index"), "Full")

    def test__get_port_duplex_half_1(self):
        """ Successfully determined duplex mode. Return Half """

        self.tested_instance.duplex_table = {"index": {"dot3StatsIndex": "port_index"}}
        self.snmp_handler.get_property.side_effect = ["halfDuplex", "empty", "unknown"]

        self.assertEqual(self.tested_instance._get_port_duplex("port_index"), "Half")
        self.assertEqual(self.tested_instance._get_port_duplex("port_index"), "Half")
        self.assertEqual(self.tested_instance._get_port_duplex("port_index"), "Half")

    def test__get_port_duplex_half_2(self):
        """ Failed to determine port duplex mode """

        self.tested_instance.duplex_table = {"index_1": {"suffix": "port_index"},
                                             "index_2": {"dot3StatsIndex": "another_port_index"}}

        self.assertEqual(self.tested_instance._get_port_duplex("port_index"), "Half")

    def test__get_port_autoneg_enabled(self):
        """ Successfully check state. Auto negotiation Enabled. Return status True """

        autoneg_status_response = {"port_index": "Autonegotiation Enabled"}
        self.snmp_handler.get = mock.MagicMock(return_value=autoneg_status_response)
        self.assertEqual(self.tested_instance._get_port_autoneg("port_index"), "True")

    def test__get_port_autoneg_disabled(self):
        """ Successfully check state. Auto negotiation Not Enabled (Unknown, Disabled etc). Return status False """

        autoneg_status_response = {"port_index": "Some autonegotiation status"}
        self.snmp_handler.get = mock.MagicMock(return_value=autoneg_status_response)
        self.assertEqual(self.tested_instance._get_port_autoneg("port_index"), "False")

    def test__get_port_autoneg_failed(self):
        """ Failed to check state. Return status False """

        self.snmp_handler.get = mock.MagicMock(side_effect=[Exception])
        self.assertEqual(self.tested_instance._get_port_autoneg("port_index"), "False")

    def test__get_adjacent_fail_empty_lldp(self):
        """ Failed to determine port adjacent. LLDP Table is empty """

        self.tested_instance.lldp_local_table = {}

        self.assertEqual(self.tested_instance._get_adjacent("interface_id"), "")

    def test__get_adjacent_fail_no_ifname(self):
        """ Failed to determine port adjacent. Can't determine interface name """

        self.tested_instance.lldp_local_table = {"iface_name_1": {"lldpLocPortDesc": "description"}}

        self.tested_instance.if_table = {"iface_id_1": {self.tested_instance.IF_ENTITY: ""}}

        self.assertEqual(self.tested_instance._get_adjacent("iface_id_1"), "")

    def test__get_adjacent_fail_ifname_not_in_lldp(self):
        """ Failed to determine port adjacent. LLDP Table doesn't content information about specified Interface name """

        self.tested_instance.lldp_local_table = {"iface_name": {"lldpLocPortDesc": "description"}}
        self.tested_instance.if_table = {"iface_id_1": {self.tested_instance.IF_ENTITY: "iface_name_1"}}

        self.assertEqual(self.tested_instance._get_adjacent("iface_id_1"), "")

    # def test__get_adjacent_fail_ifname_not_in_lldp(self):
    #     """ Failed to determine port adjacent. Can't determine interface name """
    #
    #     self.tested_instance.lldp_local_table = {"iface_name_1": {"lldpLocPortDesc": "description"}}
    #     self.tested_instance.lldp_remote_table = {"iface_name_1": {"lldpLocPortDesc": "description"}}
    #     self.tested_instance.if_table = {"iface_id_1": {self.tested_instance.IF_ENTITY: "iface_name_1"}}
    #
    #     self.assertEqual(self.tested_instance._get_adjacent("iface_id_1"), "")

    # def test__get_adjacent_fail_cant_determine_remote_port_info(self):
    #     """ Failed to determine port adjacent. Can't determine remote port information from LLDP table """
    #
    #     self.tested_instance.lldp_local_table = {"iface_name_1": {"lldpLocPortDesc": "description"}}
    #     self.tested_instance.if_table = {"iface_id_1": {self.tested_instance.IF_ENTITY: "iface_name_1"}}
    #
    #     self.assertEqual(self.tested_instance._get_adjacent("iface_id_1"), "")

    # def test__get_adjacent_success(self):
    #     """ Successfully determined port adjacent """
    #
    #     self.tested_instance.lldp_local_table = {"iface_name": {"lldpLocPortDesc": "description"}}
    #     self.tested_instance.if_table = {"iface_id_1": {self.tested_instance.IF_ENTITY: "iface_name_1"}}
    #
    #     self.assertEqual(self.tested_instance._get_adjacent("iface_id_1"), "")

    def test__get_mapping(self):
        """  """

        pass
