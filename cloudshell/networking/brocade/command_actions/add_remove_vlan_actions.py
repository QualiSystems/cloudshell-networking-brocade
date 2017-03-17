#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from cloudshell.cli.cli_service import CliService
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.networking.brocade.command_templates import add_remove_vlan as vlan_command_template


class AddRemoveVlanActions(object):
    def __init__(self, cli_service, logger):
        """ Add remove vlan

        :param cli_service: config mode cli_service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """

        self._cli_service = cli_service
        self._logger = logger

    def configure_vlan(self, vlan, action_map=None, error_map=None):
        """Create vlan entity on the device

        :param session: current session
        :param logger:  logger
        :param vlan_range: range of vlans to be created
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        """

        CommandTemplateExecutor(cli_service=self._cli_service,
                                command_template=vlan_command_template.CONFIGURE_VLAN,
                                action_map=action_map,
                                error_map=error_map).execute_command(vlan_id=vlan)

    def set_vlan_to_interface(self, tag_type, port_name, action_map=None, error_map=None):
        """ Assign vlan to a certain interface

        :param port_mode: switchport mode
        :param port_name: interface name
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        """

        output = CommandTemplateExecutor(cli_service=self._cli_service,
                                         command_template=vlan_command_template.ASSIGN_VLAN_TO_IFACE,
                                         action_map=action_map,
                                         error_map=error_map).execute_command(tag_type=tag_type, port_name=port_name)

        if re.search(r"error", output, re.IGNORECASE | re.DOTALL):
            raise Exception(self.__class__.__name__, "Error during vlan configuration. See logs for details")

    def remove_vlan_from_interface(self, vlan, tag_type, port_name, action_map=None, error_map=None):
        """ Assign vlan to a certain interface

        :param port_mode: switchport mode
        :param port_name: interface name
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        """

        output = CommandTemplateExecutor(cli_service=self._cli_service,
                                         command_template=vlan_command_template.REMOVE_VLAN_FROM_IFACE,
                                         action_map=action_map,
                                         error_map=error_map,
                                         expected_string=r"vlan\s*{0}|VLAN\s*{0}".format(vlan)).execute_command(
            tag_type=tag_type, port_name=port_name)

        if re.search(r"error", output, re.IGNORECASE | re.DOTALL):
            raise Exception(self.__class__.__name__, "Error during vlan configuration. See logs for details")
