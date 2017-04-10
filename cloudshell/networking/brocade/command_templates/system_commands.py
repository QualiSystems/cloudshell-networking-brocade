#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate

ACTION_MAP = OrderedDict([(r"(enter 'y' or 'n')", lambda session, logger: session.send_line('y'))])

COPY_TO_SECONDARY = CommandTemplate("copy {scheme} flash {host} {file_path} secondary", action_map=ACTION_MAP)
BOOT_SECONDARY = CommandTemplate("boot system flash secondary", action_map=ACTION_MAP)
COMMIT_FIRMWARE = CommandTemplate("copy flash flash primary", action_map=ACTION_MAP)
REBOOT = CommandTemplate("reload", action_map=ACTION_MAP)
