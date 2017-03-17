#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.flows.action_flows import RestoreConfigurationFlow
from cloudshell.devices.networking_utils import UrlParser
from cloudshell.networking.brocade.command_actions.save_restore_actions import SaveRestoreActions
from cloudshell.networking.brocade.command_actions.system_actions import SystemActions


class BrocadeRestoreFlow(RestoreConfigurationFlow):
    def __init__(self, cli_handler, logger):
        super(BrocadeRestoreFlow, self).__init__(cli_handler, logger)

    def execute_flow(self, path, configuration_type, restore_method, vrf_management_name):
        """ Execute flow which save selected file to the provided destination

        :param path: the path to the configuration file, including the configuration file name
        :param restore_method: the restore method to use when restoring the configuration file.
                               Possible Values are append and override
        :param configuration_type: the configuration type to restore. Possible values are startup and running
        :param vrf_management_name: Virtual Routing and Forwarding Name
        """

        _is_need_reload = False
        overwrite = False

        if not restore_method:
            restore_method = "override"

        if not configuration_type:
            configuration_type = "running-config"
        elif "-config" not in configuration_type:
            configuration_type = configuration_type.lower() + "-config"

        if configuration_type not in ["running-config", "startup-config"]:
            raise Exception(self.__class__.__name__,
                            "Device doesn't support restoring '{}' configuration type".format(configuration_type))

        connection_dict = UrlParser.parse_url(path)
        if connection_dict.get(UrlParser.PATH).endswith("/"):
            file_path = connection_dict.get(UrlParser.PATH) + connection_dict.get(UrlParser.FILENAME)
        else:
            file_path = connection_dict.get(UrlParser.PATH) + "/" + connection_dict.get(UrlParser.FILENAME)

        if configuration_type == "startup-config" and restore_method.lower() == "append":
            raise Exception(self.__class__.__name__,
                            "Device doesn't support restoring '{0}' configuration type with '{1}' method"
                            .format(configuration_type, restore_method))
        elif configuration_type == "running-config" and restore_method.lower() == "override":
            if self._cli_handler.cli_type.lower() == "console":
                overwrite = True
            else:
                _is_need_reload = True
                configuration_type = "startup-config"

        with self._cli_handler.get_cli_service(self._cli_handler.enable_mode) as enable_session:
            restore_action = SaveRestoreActions(enable_session, self._logger)
            system_action = SystemActions(enable_session, self._logger)

            restore_action.restore(config=configuration_type,
                                   protocol=connection_dict.get(UrlParser.SCHEME),
                                   host=connection_dict.get(UrlParser.HOSTNAME),
                                   file_path=file_path,
                                   overwrite=overwrite)

            if _is_need_reload:
                system_action.reboot()
