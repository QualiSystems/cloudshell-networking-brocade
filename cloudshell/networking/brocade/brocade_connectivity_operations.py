#!/usr/bin/python
# -*- coding: utf-8 -*-

import inject
import re

from cloudshell.configuration.cloudshell_cli_binding_keys import CLI_SERVICE
from cloudshell.configuration.cloudshell_shell_core_binding_keys import LOGGER, CONTEXT, API
from cloudshell.networking.operations.connectivity_operations import ConnectivityOperations
from cloudshell.networking.networking_utils import validateVlanNumber
from cloudshell.shell.core.context_utils import get_resource_context_attribute


class BrocadeConnectivityOperations(ConnectivityOperations):
    def __init__(self, context=None, api=None, cli_service=None, logger=None):
        ConnectivityOperations.__init__(self)
        self._context = context
        self._api = api
        self._cli_service = cli_service
        self._logger = logger

    @property
    def logger(self):
        return self._logger or inject.instance(LOGGER)

    @property
    def cli_service(self):
        return self._cli_service or inject.instance(CLI_SERVICE)

    @property
    def context(self):
        return self._context or inject.instance(CONTEXT)

    @property
    def api(self):
        return self._api or inject.instance(API)

    def add_vlan(self, vlan_range, port, port_mode, qnq=False, ctag=''):
        """ Configure specified vlan range in specified switchport mode on provided port

        :param vlan_range: range of VLANs to be added
        :param port: interface Resource Full Address
        :param port_mode: type of adding VLAN ('trunk' or 'access')
        :param qnq: QNQ parameter for switchport mode dot1nq
        :param ctag: CTag details
        :return: success message or Exception
        """
        self.logger.info('VLANs Configuration Started')
        self.validate_vlan_methods_incoming_parameters(vlan_range, port, port_mode)
        if_name = self.get_port_name(port)

        for vlan in self._get_vlan_list(vlan_range):
            self.cli_service.send_config_command("vlan {}".format(vlan))

            if port_mode == "trunk":
                tag_type = "tagged"
            elif port_mode == "access":
                tag_type = "untagged"
            else:
                raise Exception(self.__class__.__name__,
                                "Unsupported port mode '{}'. Should be 'trunk' or 'access'".format(port_mode))

            self.cli_service.send_config_command("{tag_type} {if_name}".format(tag_type=tag_type, if_name=if_name))
            self.cli_service.exit_configuration_mode()

            if qnq and self._does_interface_support_qnq(if_name):
                self.cli_service.send_config_command("interface {if_name}".format(if_name=if_name))
                self.cli_service.send_config_command("tag-profile enable")
                self.cli_service.exit_configuration_mode()

        return "Vlan Configuration Completed"

    def remove_vlan(self, vlan_range, port, port_mode):
        """ Remove vlan from port

        :param vlan_range: range of VLANs to be deleted
        :param port: interface Resource Full Address
        :param port_mode: type of adding vlan ('trunk' or 'access')
        :return: success message or Exception
        """
        self.logger.info('VLANs Configuration Started')
        self.validate_vlan_methods_incoming_parameters(vlan_range, port, port_mode)
        if_name = self.get_port_name(port)

        for vlan in self._get_vlan_list(vlan_range):
            self.cli_service.send_config_command("vlan {}".format(vlan))

            if port_mode == "trunk":
                tag_type = "tagged"
            elif port_mode == "access":
                tag_type = "untagged"
            else:
                raise Exception(self.__class__.__name__,
                                "Unsupported port mode '{}'. Should be 'trunk' or 'access'".format(port_mode))

            self.cli_service.send_config_command("no {tag_type} {if_name}".format(tag_type=tag_type, if_name=if_name))
            self.cli_service.exit_configuration_mode()

        return "Remove Vlan Completed"

    def validate_vlan_methods_incoming_parameters(self, vlan_range, port, port_mode):
        """Validate add_vlan and remove_vlan incoming parameters

        :param vlan_range: vlan range (10,20,30-40)
        :param port: list of port resource addresses ([192.168.1.1/0/34, 192.168.1.1/0/42])
        :param port_mode: switchport mode (access or trunk)
        """

        if not port:
            raise Exception(self.__class__.__name__, "Port can't be empty")
        if vlan_range == "" and port_mode == "access":
            raise Exception(self.__class__.__name__, "Switchport type is Access, but vlan id/range is empty")
        if ("," in vlan_range or "-" in vlan_range) and port_mode == "access":
            raise Exception(self.__class__.__name__, "Only one vlan could be assigned to the interface in Access mode")

    def _get_vlan_list(self, vlan_str):
        """ Get VLAN list from inputted string

        :param vlan_str:
        :return list of VLANs or Exception
        """

        result = set()
        for splitted_vlan in vlan_str.split(","):
            if "-" not in splitted_vlan:
                if validateVlanNumber(splitted_vlan):
                    result.add(int(splitted_vlan))
                else:
                    raise Exception(self.__class__.__name__, "Wrong VLAN number detected {}".format(splitted_vlan))
            else:
                start, end = map(int, splitted_vlan.split("-"))
                if validateVlanNumber(start) and validateVlanNumber(end):
                    if start > end:
                        start, end = end, start
                    for vlan in range(start, end+1):
                        result.add(vlan)
                else:
                    raise Exception(self.__class__.__name__, "Wrong VLANs range detected {}".format(vlan_str))

        return list(result)

    def _get_resource_full_name(self, port_resource_address, resource_details_map):
        """Recursively search for port name on the resource

        :param port_resource_address: port resource address
        :param resource_details_map: full device resource structure
        :return: full port resource name (BrocadeMLX/Chassis 0/ethernet0-23)
        """

        result = None
        for port in resource_details_map.ChildResources:
            if port.FullAddress in port_resource_address and port.FullAddress == port_resource_address:
                return port.Name
            if port.FullAddress in port_resource_address and port.FullAddress != port_resource_address:
                result = self._get_resource_full_name(port_resource_address, port)
            if result is not None:
                return result

        return result

    def get_port_name(self, port):
        """Get port name from port resource full address

        :param port: port resource full address (192.168.1.1/0/34)
        :return: port name (ethernet 0/23)
        """

        port_resource_map = self.api.GetResourceDetails(get_resource_context_attribute('name', self.context))
        temp_port_full_name = self._get_resource_full_name(port, port_resource_map)
        if not temp_port_full_name:
            err_msg = 'Failed to get port name.'
            self.logger.error(err_msg)
            raise Exception(self.__class__.__name__, err_msg)

        port_name = temp_port_full_name.split('/')[-1]
        matched = re.search(r"(?P<name>\w+)(?P<id>\d+(/\d+)*)", port_name)
        if matched:
            port_name = "{port} {id}".format(port=matched.groupdict()["name"], id=matched.groupdict()["id"])

        self.logger.info('Interface name validation OK, portname = {0}'.format(port_name))
        return port_name

    def _does_interface_support_qnq(self, interface_name):
        """ Validate whether qnq is supported for certain port """

        result = False
        self.cli_service.send_config_command('interface {0}'.format(interface_name))
        output = self.cli_service.send_config_command('tag-profile ?')
        if 'enable' in output.lower():
            result = True
        self.cli_service.exit_configuration_mode()
        return result
