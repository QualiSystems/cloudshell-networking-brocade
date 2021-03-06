#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.flows.cli_action_flows import DisableSnmpFlow
from cloudshell.networking.brocade.command_actions.enable_disable_snmp_actions import EnableDisableSnmpActions
from cloudshell.snmp.snmp_parameters import SNMPV2ReadParameters


class BrocadeDisableSnmpFlow(DisableSnmpFlow):
    def __init__(self, cli_handler, logger):
        """
          Enable snmp flow
          :param cli_handler:
          :type cli_handler: JuniperCliHandler
          :param logger:
          :return:
          """
        super(BrocadeDisableSnmpFlow, self).__init__(cli_handler, logger)
        self._cli_handler = cli_handler

    def execute_flow(self, snmp_parameters=None):
        """ Disable SNMP Read Community """

        if isinstance(snmp_parameters, SNMPV2ReadParameters) and snmp_parameters.snmp_community:
            with self._cli_handler.config_mode_service() as session:
                snmp_actions = EnableDisableSnmpActions(session, self._logger)
                self._logger.debug("Start Disable SNMP")
                snmp_actions.disable_snmp_community(snmp_parameters.snmp_community)
                snmp_actions.disable_snmp_server()
                self._logger.debug("Disable SNMP completed")

        else:
            self._logger.debug("Unsupported SNMP Version or SNMP Community is empty. Disable SNMP skipped")
