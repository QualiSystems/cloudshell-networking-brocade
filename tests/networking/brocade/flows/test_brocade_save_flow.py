#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.flows.brocade_save_flow import BrocadeSaveFlow


class TestBrocadeSaveFlow(unittest.TestCase):
    def setUp(self):
        cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        super(TestBrocadeSaveFlow, self).setUp()
        self.tested_instance = BrocadeSaveFlow(cli_handler=cli_handler, logger=logger)

    def tearDown(self):
        super(TestBrocadeSaveFlow, self).tearDown()
        del self.tested_instance

    @mock.patch("cloudshell.networking.brocade.flows.brocade_save_flow.BrocadeSaveFlow.SAVE_RESTORE_ACTIONS_CLASS")
    def test_execute_flow_success_startup(self, save_actions_class):
        """ Successfully save startup configuration """

        folder_path = "tftp://127.0.0.1/Quali_Tests"
        save_actions = mock.MagicMock()
        save_actions_class.return_value = save_actions

        self.tested_instance.execute_flow(folder_path, "startup")

        save_actions.save.assert_called_once_with(config="startup-config",
                                                  protocol="tftp",
                                                  host="127.0.0.1",
                                                  file_path="/Quali_Tests")

    @mock.patch("cloudshell.networking.brocade.flows.brocade_save_flow.BrocadeSaveFlow.SAVE_RESTORE_ACTIONS_CLASS")
    def test_execute_flow_success_default(self, save_actions_class):
        """ Successfully save running configuration as default choice """

        folder_path = "tftp://127.0.0.1/Quali_Tests"
        save_actions = mock.MagicMock()
        save_actions_class.return_value = save_actions

        self.tested_instance.execute_flow(folder_path, "")

        save_actions.save.assert_called_once_with(config="running-config",
                                                  protocol="tftp",
                                                  host="127.0.0.1",
                                                  file_path="/Quali_Tests")

    def test_execute_flow_fail_unexpected_config_type(self):
        """ Failed due to unexpected configuration type """

        folder_path = "tftp://127.0.0.1/Quali_Tests"

        with self.assertRaisesRegexp(Exception, "Device doesn't support saving"):
            self.tested_instance.execute_flow(folder_path, "unexpected-config")
