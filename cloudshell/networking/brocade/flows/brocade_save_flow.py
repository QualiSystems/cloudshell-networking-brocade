#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.flows.action_flows import SaveConfigurationFlow
from cloudshell.devices.networking_utils import UrlParser
from cloudshell.networking.brocade.command_actions.save_restore_actions import SaveRestoreActions


class BrocadeSaveFlow(SaveConfigurationFlow):
    def __init__(self, cli_handler, logger):
        super(BrocadeSaveFlow, self).__init__(cli_handler, logger)

    def execute_flow(self, folder_path, configuration_type, vrf_management_name=None):
        """ Execute flow which save selected file to the provided destination

        :param folder_path: destination path where file will be saved
        :param configuration_type: source file, which will be saved
        :param vrf_management_name: Virtual Routing and Forwarding Name
        :return: saved configuration file name
        """

        if not configuration_type:
            configuration_type = "running-config"
        elif "-config" not in configuration_type:
            configuration_type = configuration_type.lower() + "-config"

        if configuration_type not in ["running-config", "startup-config"]:
            raise Exception(self.__class__.__name__,
                            "Device doesn't support saving '{}' configuration type".format(configuration_type))

        connection_dict = UrlParser.parse_url(folder_path)

        if connection_dict.get(UrlParser.PATH).endswith("/"):
            file_path = connection_dict.get(UrlParser.PATH) + connection_dict.get(UrlParser.FILENAME)
        else:
            file_path = connection_dict.get(UrlParser.PATH) + "/" + connection_dict.get(UrlParser.FILENAME)

        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as enable_session:
            save_action = SaveRestoreActions(enable_session, self._logger)

            save_action.save(config=configuration_type,
                             protocol=connection_dict.get(UrlParser.SCHEME),
                             host=connection_dict.get(UrlParser.HOSTNAME),
                             file_path=file_path)
