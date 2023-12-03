#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (C) 2011-2023 Heiko 'riot' Weinen <riot@c-base.org> and others.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import datetime
import inspect
import pprint
import random
import string
import sys
import time
from traceback import format_exception

DEFAULT_EMITTER = "UNKNOWN"

temp = 1
events = 2
network = 4
verbose = 5
debug = 10
info = 20
warn = 30
error = 40
critical = 50
hilight = 60
version = 99
off = 100

# https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
level_data = {
    temp: ["TEMP", "\033[1;30m"],
    events: ["EVENT", "\033[1:36m"],
    verbose: ["VERB", "\033[1;30m"],
    network: ["NET", "\033[1;34m"],
    debug: ["DEBUG", "\033[1;97m"],
    info: ["INFO", "\033[1;92m"],
    warn: ["WARN", "\033[1;93m"],
    error: ["ERROR", "\033[1;31;103m"],
    critical: ["CRIT", "\033[1n\033[1;33;101m"],
    hilight: ["HILIGHT", "\033[1;4;34;106m"],
    version: ["VER", "\033[1;96;44m"],
}

terminator = "\033[0m"

process_identifier = ''.join(
    [random.choice(string.ascii_letters + string.digits) for i in range(3)])

count = 0

console = verbose

verbosity = {"global": console, "system": info, "console": console}

uncut = True
color = False

start = time.perf_counter()


def set_color(value: bool = True):
    """Activate colorful logging"""
    global color
    color = value


def set_default_emitter(value: str):
    global DEFAULT_EMITTER
    DEFAULT_EMITTER = value


def set_verbosity(global_level: int, console_level: int = None):
    """Adjust logging verbosity"""
    global verbosity

    if console_level is None:
        console_level = verbosity["console"]

    verbosity["global"] = global_level
    verbosity["console"] = console_level


# noinspection PyUnboundLocalVariable,PyIncorrectDocstring
def isolog(*what, **kwargs):
    """Logs all non keyword arguments.

    :param tuple/str what: Loggable objects (i.e. they have a string
        representation)
    :param int lvl: Debug message level
    :param str emitter: Optional log source, where this can't be determined
        automatically
    :param str sourceloc: Give specific source code location hints, used
        internally
    :param int frameref: Specify a non default frame for tracebacks
    :param bool tb: Include a traceback
    :param bool nc: Do not use color
    :param bool exc: Switch to better handle exceptions, use if logging in an
        except clause

    """

    global count
    global verbosity

    lvl = kwargs.get("lvl", info)

    if lvl < verbosity["global"]:
        return

    def assemble_things(things) -> str:
        result = ""

        for thing in things:
            result += " "
            if kwargs.get("pretty", False) and not isinstance(thing, str):
                result += "\n" + pprint.pformat(thing)
            else:
                result += str(thing)

        return result

    def write_to_console(message: str):
        try:
            print(message)
        except UnicodeEncodeError as e:
            print(message.encode("utf-8"))
            isolog("Bad encoding encountered on previous message:", e, lvl=error)
        except BlockingIOError:
            isolog("Too long log line encountered:", message[:20], lvl=warn)

    # Count all messages (missing numbers give a hint at too high log level)
    count += 1

    emitter = kwargs.get("emitter", DEFAULT_EMITTER)
    traceback = kwargs.get("tb", False)
    frame_ref = kwargs.get("frame_ref", 0)
    no_color = kwargs.get("nc", False)
    exception = kwargs.get("exc", False)

    timestamp = time.perf_counter()
    runtime = timestamp - start
    callee = None

    if exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()  # NOQA

    if verbosity["global"] <= debug or traceback:
        # Automatically log the current function details.

        if "sourceloc" not in kwargs:
            frame = kwargs.get("frame", frame_ref)

            # Get the previous frame in the stack, otherwise it would
            # be this function
            current_frame = inspect.currentframe()
            while frame > 0:
                frame -= 1
                current_frame = current_frame.f_back

            func = current_frame.f_code
            # Dump the message + the name of this function to the log.

            if exception:
                # noinspection PyUnboundLocalVariable
                line_no = exc_tb.tb_lineno
                if lvl <= error:
                    lvl = error
            else:
                line_no = func.co_firstlineno

            callee = "[%.10s@%s:%i]" % (func.co_name, func.co_filename, line_no)
        else:
            callee = kwargs["sourceloc"]

    now = datetime.datetime.now().isoformat()
    msg = "[%s]:[%s]:%s:%.5f:%3i: [%5s]" % (
        now,
        process_identifier,
        level_data[lvl][0],
        runtime,
        count,
        emitter,
    )

    if callee:
        if not uncut and lvl > 10:
            msg += "%-60s" % callee
        else:
            msg += "%s" % callee

    content = assemble_things(what)
    msg += content

    if exception:
        msg += "\n" + "".join(format_exception(exc_type, exc_obj, exc_tb))

    if not uncut and lvl > 10 and len(msg) > 1000:
        msg = msg[:1000]

    if lvl >= verbosity["console"]:
        output = str(msg)
        if color and not no_color:
            output = level_data[lvl][1] + output + terminator
        write_to_console(output)
