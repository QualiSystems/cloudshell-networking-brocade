#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.command_actions.save_restore_actions import SaveRestoreActions


class TestSaveRestoreActions(unittest.TestCase):
    def setUp(self):
        cli_service = mock.MagicMock()
        logger = mock.MagicMock()
        super(TestSaveRestoreActions, self).setUp()
        self.tested_instance = SaveRestoreActions(cli_service=cli_service, logger=logger)

    def tearDown(self):
        super(TestSaveRestoreActions, self).tearDown()
        del self.tested_instance

    @mock.patch("cloudshell.networking.brocade.command_actions.save_restore_actions.CommandTemplateExecutor")
    def test_save_fail_specific_error_info(self, executor_class):
        """ Failed to save configuration. Determine error message from output """

        executor = mock.MagicMock()
        executor_class.return_value = executor

        err_msg = "some error during saving configuration"

        executor.execute_command.return_value = "TFTP: {}".format(err_msg)

        with self.assertRaisesRegexp(Exception, err_msg):
            self.tested_instance.save("config", "protocol", "host", "file_path")

    @mock.patch("cloudshell.networking.brocade.command_actions.save_restore_actions.CommandTemplateExecutor")
    def test_save_fail_general_error(self, executor_class):
        """ Failed to save configuration. Can't determine error from output, return general error info """

        executor = mock.MagicMock()
        executor_class.return_value = executor

        executor.execute_command.return_value = "some error during save configuration operation"

        with self.assertRaisesRegexp(Exception, "Save device configuration failed"):
            self.tested_instance.save("config", "protocol", "host", "file_path")
