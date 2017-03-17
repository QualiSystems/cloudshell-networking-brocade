#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.command_template.command_template import CommandTemplate


CONFIGURE_VLAN = CommandTemplate("vlan {vlan_id}")
CONFIGURE_VLAN_RANGE = CommandTemplate("vlan {start_vlan} to {end_vlan}")
ASSIGN_VLAN_TO_IFACE = CommandTemplate("{tag_type} {port_name}")
REMOVE_VLAN_FROM_IFACE = CommandTemplate("no {tag_type} {port_name}")
