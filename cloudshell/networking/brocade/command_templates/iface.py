#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.command_template.command_template import CommandTemplate


CONFIGURE_IFACE = CommandTemplate("interface {port_name}")
GET_TAG_PROFILE = CommandTemplate("tag-profile ?")
ENABLE_TAG_PROFILE = CommandTemplate("tag-profile enable")
