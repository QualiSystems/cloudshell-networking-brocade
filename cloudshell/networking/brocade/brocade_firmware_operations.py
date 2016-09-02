#!/usr/bin/python
# -*- coding: utf-8 -*-

import inject


from cloudshell.configuration.cloudshell_cli_binding_keys import CLI_SERVICE
from cloudshell.configuration.cloudshell_shell_core_binding_keys import LOGGER, CONTEXT, API
from cloudshell.networking.brocade.brocade_state_operations import BrocadeStateOperations
from cloudshell.networking.networking_utils import UrlParser
from cloudshell.networking.operations.interfaces.firmware_operations_interface import FirmwareOperationsInterface
from cloudshell.shell.core.config_utils import override_attributes_from_config


class BrocadeFirmwareOperations(FirmwareOperationsInterface):
    DEFAULT_PROMPT = r'[>$#]\s*$'

    def __init__(self, context=None, api=None, cli_service=None, logger=None):
        self._context = context
        self._api = api
        self._cli_service = cli_service
        self._logger = logger
        overridden_config = override_attributes_from_config(BrocadeFirmwareOperations)
        self._default_prompt = overridden_config.DEFAULT_PROMPT

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

    @property
    def state_operations(self):
        return BrocadeStateOperations()

    def load_firmware(self, path, vrf_management_name):
        """ Update firmware version on device by loading provided image, performs following steps:
         1. Copy bin file to SECONDARY partition from remote tftp server.
         2. Set SECONDARY partition as boot
         3. Reboot device.
         4. Check if firmware was installed successfully.
         5. If firmware was installed successfully then copy SECONDARY partition to PRIMARY

         :param path: full path to firmware file on ftp/tftp location
         :param vrf_management_name: VRF Name
         :return: status / exception
         """

        connection_dict = UrlParser.parse_url(path)
        if connection_dict.get(UrlParser.PATH).endswith("/"):
            file_path = connection_dict.get(UrlParser.PATH) + connection_dict.get(UrlParser.FILENAME)
        else:
            file_path = connection_dict.get(UrlParser.PATH) + "/" + connection_dict.get(UrlParser.FILENAME)

        copy_firmware_command = "copy {scheme} flash {host} {file_path} secondary delete-first"\
            .format(scheme=connection_dict.get(UrlParser.SCHEME),
                    host=connection_dict.get(UrlParser.HOSTNAME),
                    file_path=file_path)

        output = self.cli_service.send_command(command=copy_firmware_command, expected_str=self._default_prompt)

        self.cli_service.send_config_command(command="boot system flash secondary", expected_str=self._default_prompt)
        self.cli_service.exit_configuration_mode()
        self.state_operations.reload()
        self.cli_service.send_config_command(command="copy flash flash primary delete-first",
                                             expected_str=self._default_prompt)
