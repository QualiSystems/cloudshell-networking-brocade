#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.command_template.command_template import CommandTemplate


SAVE = CommandTemplate("copy {config} {protocol} {host} {file_path}")
RESTORE = CommandTemplate("copy {protocol} {config} {host} {file_path} [overwrite{overwrite}]")
