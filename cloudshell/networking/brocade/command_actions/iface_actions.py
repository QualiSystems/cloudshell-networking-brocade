#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.networking.brocade.command_templates import iface as iface_command_template


class IFaceActions(object):
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

    def get_port_name(self, port):
        """ Get port name from port resource full address

        :param port: port resource full address (192.168.1.1/0/34)
        :return: port name (FastEthernet0/23)
        :rtype: string
        """

        if not port:
            err_msg = 'Failed to get port name.'
            self._logger.error(err_msg)
            raise Exception(self.__class__.__name__, err_msg)

        port_name = port.split('/')[-1]
        matched = re.search(r"(?P<name>\w+)(?P<id>\d+(/\d+)*)", port_name.replace("-", "/"))
        if matched:
            port_name = "{port} {id}".format(port=matched.groupdict()["name"], id=matched.groupdict()["id"])

        self._logger.info('Interface name validation OK, portname = {0}'.format(port_name))
        return port_name

    def does_interface_support_qnq(self, port_name, action_map=None, error_map=None):
        """ Validate whether qnq is supported for certain port """

        CommandTemplateExecutor(cli_service=self._cli_service,
                                command_template=iface_command_template.CONFIGURE_IFACE,
                                action_map=action_map,
                                error_map=error_map).execute_command(port_name=port_name)

        output = CommandTemplateExecutor(cli_service=self._cli_service,
                                         command_template=iface_command_template.GET_TAG_PROFILE,
                                         action_map=action_map,
                                         error_map=error_map).execute_command()

        self._cli_service.send_line("end", self._logger)

        if 'enable' in output.lower():
            return True

        return False

    def enable_qnq(self, port_name, action_map=None, error_map=None):
        """

        :param port_name: Interface name
        :param action_map:
        :param error_map:
        :return:
        """

        CommandTemplateExecutor(cli_service=self._cli_service,
                                command_template=iface_command_template.CONFIGURE_IFACE,
                                action_map=action_map,
                                error_map=error_map).execute_command(port_name=port_name)

        CommandTemplateExecutor(cli_service=self._cli_service,
                                command_template=iface_command_template.ENABLE_TAG_PROFILE,
                                action_map=action_map,
                                error_map=error_map).execute_command()
