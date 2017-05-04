#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.flows.brocade_restore_flow import BrocadeRestoreFlow


class TestBrocadeRestoreFlow(unittest.TestCase):
    def setUp(self):
        super(TestBrocadeRestoreFlow, self).setUp()
        self.cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        self.tested_instance = BrocadeRestoreFlow(cli_handler=self.cli_handler, logger=logger)

    def tearDown(self):
        super(TestBrocadeRestoreFlow, self).tearDown()
        del self.tested_instance

    def test_execute_flow_fail_unexpected_config_type(self):
        """ Failed due to unexpected configuration type """

        folder_path = "tftp://127.0.0.1/Quali_Tests"

        with self.assertRaisesRegexp(Exception, "Device doesn't support restoring .* configuration type"):
            self.tested_instance.execute_flow(folder_path, "unexpected-config", "restore_method")

    def test_execute_flow_fail_startup_append_not_supported(self):
        """ Failed due to ustartup configuration type can't be restored using append method """

        folder_path = "tftp://127.0.0.1/Quali_Tests"

        with self.assertRaisesRegexp(Exception, "Device doesn't support restoring .*configuration type with .* method"):
            self.tested_instance.execute_flow(folder_path, "startup-config", "append")

    @mock.patch("cloudshell.networking.brocade.flows.brocade_restore_flow.SystemActions")
    @mock.patch("cloudshell.networking.brocade.flows.brocade_restore_flow.BrocadeRestoreFlow.SAVE_RESTORE_ACTIONS_CLASS")
    def test_execute_flow_success_running_override_console(self, restore_actions_class, system_actions_class):
        """ Successfully restore running configuration using override method and console connection """

        folder_path = "tftp://127.0.0.1/Quali_Tests"
        configuration_type = "running-config"
        restore_method = "override"

        restore_actions = mock.MagicMock()
        restore_actions_class.return_value = restore_actions

        system_actions = mock.MagicMock()
        system_actions_class.return_value = system_actions

        self.cli_handler.cli_type = "console"

        self.tested_instance.execute_flow(folder_path, configuration_type, restore_method)

        restore_actions.restore.assert_called_once_with(config=configuration_type,
                                                        protocol="tftp",
                                                        host="127.0.0.1",
                                                        file_path="/Quali_Tests",
                                                        overwrite=True)
        system_actions.reboot.assert_not_called()

    @mock.patch("cloudshell.networking.brocade.flows.brocade_restore_flow.SystemActions")
    @mock.patch("cloudshell.networking.brocade.flows.brocade_restore_flow.BrocadeRestoreFlow.SAVE_RESTORE_ACTIONS_CLASS")
    def test_execute_flow_success_running_override_not_console(self, restore_actions_class, system_actions_class):
        """ Successfully restore running configuration using override method and non console connection """

        folder_path = "tftp://127.0.0.1/Quali_Tests"
        configuration_type = "running-config"
        restore_method = "override"

        restore_actions = mock.MagicMock()
        restore_actions_class.return_value = restore_actions

        system_actions = mock.MagicMock()
        system_actions_class.return_value = system_actions

        self.cli_handler.cli_type = "not_console"

        self.tested_instance.execute_flow(folder_path, configuration_type, restore_method)

        restore_actions.restore.assert_called_once_with(config="startup-config",
                                                        protocol="tftp",
                                                        host="127.0.0.1",
                                                        file_path="/Quali_Tests",
                                                        overwrite=False)

        system_actions.reboot.assert_called_once()
