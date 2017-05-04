#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.flows.brocade_load_firmware_flow import BrocadeLoadFirmwareFlow


class TestBrocadeLoadFirmwareFlow(unittest.TestCase):
    def setUp(self):
        super(TestBrocadeLoadFirmwareFlow, self).setUp()
        self.cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        self.tested_instance = BrocadeLoadFirmwareFlow(cli_handler=self.cli_handler, logger=logger)

    def tearDown(self):
        super(TestBrocadeLoadFirmwareFlow, self).tearDown()
        del self.tested_instance

    @mock.patch("cloudshell.networking.brocade.flows.brocade_load_firmware_flow.UrlParser")
    def test_execute_flow_fail_no_firmware_file(self, url_class):
        """  """

        url_parser = mock.MagicMock()
        url_class.return_value = url_parser
        url_parser.parse_url.return_value = dict()

        with self.assertRaisesRegexp(Exception, "Unable to find firmware file"):
            self.tested_instance.execute_flow("path", "vrf", "timeout")

    @mock.patch("cloudshell.networking.brocade.flows.brocade_load_firmware_flow.BrocadeLoadFirmwareFlow.SYSTEM_ACTIONS_CLASS")
    def test_execute_flow_success(self, system_actions_class):
        """  """

        system_actions = mock.MagicMock()
        system_actions_class.return_value = system_actions
        firmware_file_path = "tftp://127.0.0.1/Quali_Tests/firmware.file"

        self.tested_instance.execute_flow(firmware_file_path, "", 5)
        system_actions.load_firmware.assert_called_once_with(protocol="tftp",
                                                             host="127.0.0.1",
                                                             file_path="/Quali_Tests/firmware.file")
