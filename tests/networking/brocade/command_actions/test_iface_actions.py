#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.command_actions.iface_actions import IFaceActions


class TestIFaceActions(unittest.TestCase):
    def setUp(self):
        cli_service = mock.MagicMock()
        logger = mock.MagicMock()
        super(TestIFaceActions, self).setUp()
        self.tested_instance = IFaceActions(cli_service=cli_service, logger=logger)

    def tearDown(self):
        super(TestIFaceActions, self).tearDown()
        del self.tested_instance

    def test_get_port_name_empty_port_value(self):
        """ Raise Exception because port is empty or None """
        with self.assertRaisesRegexp(Exception, "Failed to get port name."):
            self.tested_instance.get_port_name(port=None)
        with self.assertRaisesRegexp(Exception, "Failed to get port name."):
            self.tested_instance.get_port_name(port="")

    def test_get_port_name_portchannel(self):
        """ Successfully return port-channel name """

        self.assertEqual(self.tested_instance.get_port_name("CH1/M1/port-channel-4"), "port-channel-4")

    def test_get_port_name_portname(self):
        """ Successfully return port name """

        self.assertEqual(self.tested_instance.get_port_name("CH1/M1/Ethernet-4"), "Ethernet-4")
