#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.flows.action_flows import LoadFirmwareFlow
from cloudshell.devices.networking_utils import UrlParser
from cloudshell.networking.brocade.command_actions.system_actions import SystemActions


class BrocadeLoadFirmwareFlow(LoadFirmwareFlow):
    SYSTEM_ACTIONS_CLASS = SystemActions

    def __init__(self, cli_handler, logger):
        super(BrocadeLoadFirmwareFlow, self).__init__(cli_handler, logger)

    def execute_flow(self, path, vrf, timeout):
        """Load a firmware onto the device

        :param path: The path to the firmware file, including the firmware file name
        :param vrf: Virtual Routing and Forwarding Name
        :param timeout:
        :return:
        """

        full_path_dict = UrlParser().parse_url(path)
        firmware_file_name = full_path_dict.get(UrlParser.FILENAME)
        if not firmware_file_name:
            raise Exception(self.__class__.__name__, "Unable to find firmware file")

        connection_dict = UrlParser.parse_url(path)
        if connection_dict.get(UrlParser.PATH).endswith("/"):
            file_path = connection_dict.get(UrlParser.PATH) + connection_dict.get(UrlParser.FILENAME)
        else:
            file_path = connection_dict.get(UrlParser.PATH) + "/" + connection_dict.get(UrlParser.FILENAME)

        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as enable_session:
            system_action = self.SYSTEM_ACTIONS_CLASS(enable_session, self._logger)

            try:
                return system_action.load_firmware(protocol=connection_dict.get(UrlParser.SCHEME),
                                                   host=connection_dict.get(UrlParser.HOSTNAME),
                                                   file_path=file_path)
            except:
                raise
