#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.command_actions.system_actions import SystemActions


class TestSystemActions(unittest.TestCase):
    def setUp(self):
        self.cli_service = mock.MagicMock()
        logger = mock.MagicMock()
        super(TestSystemActions, self).setUp()
        self.tested_instance = SystemActions(cli_service=self.cli_service, logger=logger)

    def tearDown(self):
        super(TestSystemActions, self).tearDown()
        del self.tested_instance

    @mock.patch("cloudshell.networking.brocade.command_actions.system_actions.CommandTemplateExecutor")
    def test_reboot_success_console_session(self, executor_class):
        """ Successfully reboot the system using console session """

        executor = mock.MagicMock()
        executor_class.return_value = executor
        executor.execute_command = mock.MagicMock()
        self.cli_service.session.session_type = "console"

        self.tested_instance.reboot()

        executor.execute_command.assert_called_once_with()
        self.cli_service.reconnect.assert_not_called()

    @mock.patch("cloudshell.networking.brocade.command_actions.system_actions.CommandTemplateExecutor")
    def test_reboot_success_non_console_session(self, executor_class):
        """ Successfully reboot the system using non-console session """

        executor = mock.MagicMock()
        executor_class.return_value = executor
        executor.execute_command = mock.MagicMock()
        self.cli_service.session.session_type = "not_console"

        self.tested_instance.reboot()

        executor.execute_command.assert_called_once_with()
        self.cli_service.reconnect.assert_called_once_with(timeout=self.tested_instance.SESSION_RECONNECT_TIMEOUT)

    @mock.patch("cloudshell.networking.brocade.command_actions.system_actions.CommandTemplateExecutor")
    def test_load_firmware_success_console_session(self, executor_class):
        """ Successfully load firmware using console session """

        executor = mock.MagicMock()
        executor_class.return_value = executor
        executor.execute_command = mock.MagicMock(side_effect=["TFTP copy image done", "some_response_2", "Done"])
        self.cli_service.session.session_type = "console"

        self.tested_instance.load_firmware("protocol", "host", "file_path")

        self.assertEqual(executor.execute_command.call_count, 3)

        executor.execute_command.assert_has_calls([mock.call.execute_command(scheme="protocol",
                                                                             host="host",
                                                                             file_path="file_path"),
                                                   mock.call.execute_command(),
                                                   mock.call.execute_command()])

        self.cli_service.reconnect.assert_not_called()

    @mock.patch("cloudshell.networking.brocade.command_actions.system_actions.CommandTemplateExecutor")
    def test_load_firmware_success_non_console_session(self, executor_class):
        """ Successfully load firmware using non-console session """

        executor = mock.MagicMock()
        executor_class.return_value = executor
        executor.execute_command = mock.MagicMock(side_effect=["TFTP copy image done", "some_response_2", "Done"])
        self.cli_service.session.session_type = "non_console"

        self.tested_instance.load_firmware("protocol", "host", "file_path")

        self.assertEqual(executor.execute_command.call_count, 3)

        executor.execute_command.assert_has_calls([mock.call.execute_command(scheme="protocol",
                                                                             host="host",
                                                                             file_path="file_path"),
                                                   mock.call.execute_command(),
                                                   mock.call.execute_command()])

        self.cli_service.reconnect.assert_called_once_with(timeout=self.tested_instance.SESSION_RECONNECT_TIMEOUT)

    @mock.patch("cloudshell.networking.brocade.command_actions.system_actions.CommandTemplateExecutor")
    def test_load_firmware_fail_specific_error_info(self, executor_class):
        """ Failed copy firmware image from remote to secondary. Specific error determined """

        executor = mock.MagicMock()
        executor_class.return_value = executor

        err_msg = "some error during load image to secondary "

        executor.execute_command.return_value = "TFTP: {}".format(err_msg)

        with self.assertRaisesRegexp(Exception, err_msg):
            self.tested_instance.load_firmware("protocol", "host", "file_path")

        self.assertEqual(executor.execute_command.call_count, 1)

    @mock.patch("cloudshell.networking.brocade.command_actions.system_actions.CommandTemplateExecutor")
    def test_load_firmware_fail_general_error_info(self, executor_class):
        """ Failed copy firmware image from remote to secondary. General error """

        executor = mock.MagicMock()
        executor_class.return_value = executor

        err_msg = "some error during load image to secondary "

        executor.execute_command.return_value = err_msg

        with self.assertRaisesRegexp(Exception, "Error during copy firmware image"):
            self.tested_instance.load_firmware("protocol", "host", "file_path")

    @mock.patch("cloudshell.networking.brocade.command_actions.system_actions.CommandTemplateExecutor")
    def test_load_firmware_fail_copy_to_primary(self, executor_class):
        """ Failed copy secondary to primary """

        executor = mock.MagicMock()
        executor_class.return_value = executor

        executor.execute_command = mock.MagicMock(side_effect=["TFTP copy image done",
                                                               "some_response_1",
                                                               "some_response_2"])

        with self.assertRaisesRegexp(Exception, "Load firmware failed during copy from secondary to primary"):
            self.tested_instance.load_firmware("protocol", "host", "file_path")

        executor.execute_command.assert_has_calls([mock.call.execute_command(scheme="protocol",
                                                                             host="host",
                                                                             file_path="file_path"),
                                                   mock.call.execute_command(),
                                                   mock.call.execute_command()])
