#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.command_template.command_template import CommandTemplate


DISPLAY_PASSWORD = CommandTemplate("enable password-display")
SHOW_SNMP_INFO = CommandTemplate("show snmp server")
ENABLE_SNMP = CommandTemplate("snmp-server")
ENABLE_SNMP_READ_COMMUNITY = CommandTemplate("snmp-server community {snmp_community} ro")
DISABLE_SNMP_READ_COMMUNITY = CommandTemplate("no snmp-server community {snmp_community} ro")
DISABLE_SNMP = CommandTemplate("no snmp-server")
