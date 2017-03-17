#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.networking.brocade.command_templates import system_commands


class SystemActions(object):
    SESSION_RECONNECT_TIMEOUT = 180

    def __init__(self, cli_service, logger):
        """ Reboot actions

        :param cli_service: default mode cli_service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """

        self._cli_service = cli_service
        self._logger = logger

    def reboot(self, action_map=None, error_map=None):
        """ Reboot the system """

        try:
            CommandTemplateExecutor(cli_service=self._cli_service,
                                    command_template=system_commands.REBOOT,
                                    action_map=action_map,
                                    error_map=error_map,
                                    expected_string="Halt and reboot").execute_command()
        except Exception as e:
            self._logger.info("Session type is '{}', closing session...".format(self._cli_service.session.session_type))

        if self._cli_service.session.session_type.lower() != "console":
            self._cli_service.reconnect(timeout=self.SESSION_RECONNECT_TIMEOUT)

    def load_firmware(self, protocol, host, file_path, action_map=None, error_map=None):
        """ Upgrade firmware """

        output = CommandTemplateExecutor(cli_service=self._cli_service,
                                         command_template=system_commands.COPY_TO_SECONDARY,
                                         action_map=action_map,
                                         error_map=error_map).execute_command(scheme=protocol,
                                                                              host=host,
                                                                              file_path=file_path)
        output = self._buffer_readup(output=output)

        if re.search(r"TFTP.*done", output):
            self._logger.debug("Copy new image to flash secondary successfully")
            self._logger.debug("Try boot device from secondary flash ...")
            try:
                CommandTemplateExecutor(cli_service=self._cli_service,
                                        command_template=system_commands.BOOT_SECONDARY,
                                        action_map=action_map,
                                        error_map=error_map).execute_command()
            except Exception as e:
                self._logger.info("Session type is '{}', closing session...".format(self._cli_service.session.session_type))

            if self._cli_service.session.session_type.lower() != "console":
                self._cli_service.reconnect(timeout=self.SESSION_RECONNECT_TIMEOUT)

            self._logger.debug("Boot from secondary flash successfully. Copy Secondary to Primary ...")

            output = CommandTemplateExecutor(cli_service=self._cli_service,
                                             command_template=system_commands.COMMIT_FIRMWARE,
                                             action_map=action_map,
                                             error_map=error_map).execute_command()

            output = self._buffer_readup(output=output)

            if not re.search(r"Done", output, re.IGNORECASE):
                raise Exception(self.__class__.__name__, "Load firmware failed during copy from secondary to primary")

            return "Update firmware completed successfully"
        else:
            matched = re.match(r"TFTP:.*", output)
            if matched:
                error = matched.group()
            else:
                error = "Error during copy firmware image"
            raise Exception(self.__class__.__name__, "Load firmware failed with error: {}".format(error))

    def _buffer_readup(self, output):
        """ Read buffer to end of command execution if prompt returned immediately """

        return output

    def shutdown(self, action_map=None, error_mapp=None):
        """ Shutdown the system """

        pass
