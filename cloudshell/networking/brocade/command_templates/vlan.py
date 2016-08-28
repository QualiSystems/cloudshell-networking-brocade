#!/usr/bin/env python
# -*- coding: utf-8 -*-


from cloudshell.cli.command_template.command_template import CommandTemplate
from cloudshell.networking.networking_utils import validateIP, validateVlanRange


VLAN_COMMANDS_TEMPLATES = {
    'configure_vlan': CommandTemplate('vlan {0}', validateVlanRange, "Cannot create vlan - wrong vlan number(s)"),
    'quit': CommandTemplate('quit'),
    'allow_access_vlan': CommandTemplate('untagged ethernet {0}', [r".+"], ["Interface name is incorrect!"]),
    'allow_trunk_vlan': CommandTemplate('tagged ethernet {0}', [r".+"], ["Interface name is incorrect!"]),
    'allow_trunk_vlan_range': CommandTemplate('tagged ethernet {0} to {1}', [r".+", r".+"],
                                              ["Interface name is incorrect!", "Interface name is incorrect!"]),
}