#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.cli_service_impl import CliServiceImpl as CliService
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.networking.brocade.command_templates import enable_disable_snmp


class EnableDisableSnmpActions(object):
    def __init__(self, cli_service, logger):
        """
        Reboot actions
        :param cli_service: config mode cli service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """
        self._cli_service = cli_service
        self._logger = logger

    def get_current_snmp_info(self, action_map=None, error_map=None):
        """ Retrieve current SNMP information like SNMP Server status and Read Communities

        :param cli_service:
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        :return:
        :rtype: str
        """

        CommandTemplateExecutor(cli_service=self._cli_service,
                                command_template=enable_disable_snmp.DISPLAY_PASSWORD,
                                action_map=action_map,
                                error_map=error_map).execute_command()

        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=enable_disable_snmp.SHOW_SNMP_INFO,
                                       action_map=action_map,
                                       error_map=error_map).execute_command()

    def enable_snmp_server(self, action_map=None, error_map=None):
        """Enable SNMP on the device

        :param cli_service:
        :param snmp_community: community name
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        """

        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=enable_disable_snmp.ENABLE_SNMP,
                                       action_map=action_map,
                                       error_map=error_map).execute_command()

    def enable_snmp_community(self, snmp_community, action_map=None, error_map=None):
        """Enable SNMP on the device

        :param cli_service:
        :param snmp_community: community name
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        """

        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=enable_disable_snmp.ENABLE_SNMP_READ_COMMUNITY,
                                       action_map=action_map,
                                       error_map=error_map).execute_command(snmp_community=snmp_community)

    def disable_snmp_community(self, snmp_community, action_map=None, error_map=None):
        """Enable SNMP on the device

        :param cli_service:
        :param snmp_community: community name
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        """

        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=enable_disable_snmp.DISABLE_SNMP_READ_COMMUNITY,
                                       action_map=action_map,
                                       error_map=error_map).execute_command(snmp_community=snmp_community)

    def disable_snmp_server(self, action_map=None, error_map=None):
        """Disable SNMP on the device

        :param cli_service:
        :param snmp_community: community name
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        """

        return CommandTemplateExecutor(cli_service=self._cli_service,
                                       command_template=enable_disable_snmp.DISABLE_SNMP,
                                       action_map=action_map,
                                       error_map=error_map).execute_command()
