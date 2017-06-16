#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
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

    def test__get_ipv4_interface_address(self):
        """  """

        pass

    def test__get_ipv6_interface_address(self):
        """  """

        pass

    def test__get_port_duplex(self):
        """  """

        pass

    def test__get_port_autoneg(self):
        """  """

        pass

    def test__get_adjacent(self):
        """  """

        pass

    def test__get_mapping(self):
        """  """

        pass
