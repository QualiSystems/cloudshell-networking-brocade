#!/usr/bin/python
# -*- coding: utf-8 -*-

import inject
import re
import time


from cloudshell.configuration.cloudshell_cli_binding_keys import CLI_SERVICE, SESSION
from cloudshell.configuration.cloudshell_shell_core_binding_keys import LOGGER, CONTEXT, API

from cloudshell.networking.operations.interfaces.configuration_operations_interface import \
    ConfigurationOperationsInterface
from cloudshell.shell.core.config_utils import override_attributes_from_config
from cloudshell.shell.core.context_utils import get_resource_name


class BrocadeConfigurationOperations(ConfigurationOperationsInterface):
    DEFAULT_PROMPT = r'[>$#]\s*$'
    SESSION_WAIT_TIMEOUT = 600
    SAVE_RESPONSE_TIMEOUT = 3
    SAVE_RESPONSE_RETRIES = 10

    def __init__(self, context=None, api=None, cli_service=None, logger=None):
        self._context = context
        self._api = api
        self._cli_service = cli_service
        self._logger = logger
        overridden_config = override_attributes_from_config(BrocadeConfigurationOperations)
        self._default_prompt = overridden_config.DEFAULT_PROMPT
        self._session_wait_timeout = overridden_config.SESSION_WAIT_TIMEOUT
        self._save_response_timeout = overridden_config.SAVE_RESPONSE_TIMEOUT
        self._save_response_retries = overridden_config.SAVE_RESPONSE_RETRIES
        try:
            self.resource_name = re.sub(r'[\.\s]', '_', get_resource_name())
        except Exception:
            raise Exception(self.__class__.__name__, 'ResourceName is empty or None')

    @property
    def api(self):
        return self._api or inject.instance(API)

    @property
    def cli_service(self):
        return self._cli_service or inject.instance(CLI_SERVICE)

    @property
    def logger(self):
        return self._logger or inject.instance(LOGGER)

    @property
    def context(self):
        return self._context or inject.instance(CONTEXT)

    @property
    def session(self):
        return inject.instance(SESSION)

    def restore_configuration(self, source_file, config_type, restore_method='override', vrf=None):
        """ General method for restore configuration on Brocade devices """
        pass

    def save_configuration(self, destination_host, source_filename, vrf=None):
        """ General method for save configuration on Brocade devices """
        pass

    def reload(self):
        """ Reload device """

        expected_map = {"(enter 'y' or 'n')": lambda session: session.send_line('y')}
        try:
            self.logger.info("Send 'reload' to device...")
            self.cli_service.send_command(command='reload', expected_map=expected_map, timeout=3)
        except Exception as e:
            self.logger.info('Session type is \'{}\', closing session...'.format(self.session.session_type))

        if self.session.session_type.lower() != 'console':
            self._wait_for_session_restore(self.session)

    def _wait_for_session_restore(self, session):
        """ Wait for restore session connection """

        self.logger.debug('Waiting session restore')
        waiting_reboot_time = time.time()
        while True:
            try:
                if time.time() - waiting_reboot_time > self._session_wait_timeout:
                    raise Exception(self.__class__.__name__,
                                    "Session doesn't closed in {} sec as expected".format(
                                        self._session_wait_timeout))
                session.send_line('')
                time.sleep(1)
            except:
                self.logger.debug('Session disconnected')
                break
        reboot_time = time.time()
        while True:
            if time.time() - reboot_time > self._session_wait_timeout:
                self.cli_service.destroy_threaded_session(session=session)
                raise Exception(self.__class__.__name__,
                                'Session cannot connect after {} sec.'.format(self._session_wait_timeout))
            try:
                self.logger.debug('Reconnect retry')
                session.connect(re_string=self._default_prompt)
                self.logger.debug('Session connected')
                break
            except:
                time.sleep(5)