#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell.networking.brocade.cli.brocade_cli_handler import BrocadeCliHandler
from cloudshell.networking.brocade.runners.brocade_state_runner import BrocadeStateRunner


class TestBrocadeStateRunner(unittest.TestCase):
    def setUp(self):
        cli_handler = mock.MagicMock()
        logger = mock.MagicMock()
        resource_config = mock.MagicMock()
        api = mock.MagicMock()
        super(TestBrocadeStateRunner, self).setUp()
        self.tested_instance = BrocadeStateRunner(cli=cli_handler,
                                                  logger=logger,
                                                  resource_config=resource_config,
                                                  api=api)

    def tearDown(self):
        super(TestBrocadeStateRunner, self).tearDown()
        del self.tested_instance

    def test_cli_handler_property(self):
        """ Check that property return correct instance. Should return BrocadeCliHandler """

        self.assertIsInstance(self.tested_instance.cli_handler, BrocadeCliHandler)
