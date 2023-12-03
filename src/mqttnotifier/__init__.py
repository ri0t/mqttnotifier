#!/bin/env python3

#  mqttnotifier - __init__.py
#  Copyright (c) 2023. Heiko 'riot' Weinen <riot@c-base.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
import random
import sys
from configparser import ConfigParser
from getpass import getpass
from json import dumps, loads, JSONDecodeError

import plyer
import rich_click as click
from paho.mqtt import client as mqtt_client

from mqttnotifier.logger import isolog as log, set_verbosity, verbose, debug, warn, error, set_color, \
    set_default_emitter, hilight, info
from mqttnotifier.scm_version import version

DEFAULT_CFG = "~/.config/mqttnotifier/config.toml"
DEFAULT_SERVER = "127.0.0.1"
DEFAULT_PORT = 1883
DEFAULT_TOPIC = "mqttnotifier/notifications"
DEFAULT_TITLE = "MQTT Notification"
DEFAULT_APPNAME = "MQTTNotifier"
DEFAULT_APPICON = "dialog-information"
DEFAULT_TIMEOUT = 15


def connect_mqtt(broker, port, client_id, username="", password=""):
    """Connect to the mqtt broker and return a usable client"""

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log("Connected to MQTT Broker!", lvl=debug)
        else:
            log(f"Failed to connect, return code {rc}", lvl=error)

    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    if username != "":
        log(f"Using username {username}", lvl=debug)
        client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)

    return client


def configure(ctx, param, configuration_filename):
    """Parse configuration file into click context"""

    filename = os.path.expanduser(configuration_filename)

    cfg = ConfigParser()
    cfg.read(filename)
    ctx.default_map = {}
    for sect in cfg.sections():
        command_path = sect.split('.')
        if command_path[0] != 'options':
            continue
        defaults = ctx.default_map
        for command_name in command_path[1:]:
            defaults = defaults.setdefault(command_name, {})
        defaults.update(cfg[sect])


def subscribe(client: mqtt_client, topic: str):
    """Subscribes to a given topic using the connected client"""

    def on_message(receiving_client, userdata, msg):
        """Process incoming notifications"""

        log("Received notification")
        try:
            data = loads(msg.payload.decode())
        except JSONDecodeError as e:
            log("Error decoding json:", e, exc=True)
            log("Offending message:", msg.payload.decode(), lvl=error)

        log(f"Received `{data}` from `{msg.topic}` topic", lvl=debug)
        plyer.notification.notify(**data)

    client.subscribe(topic)
    client.on_message = on_message
    log(f"Subscribed to {topic}", lvl=debug)


def publish_test_message(client: mqtt_client, topic: str, **kwargs):
    """Transmits a test message with given properties (kwargs) to the MQTT broker"""

    log(f"Publishing test message to {topic}: {kwargs['message']}", lvl=verbose)
    show = kwargs.pop('show', False)
    payload = dumps(kwargs)

    if show is True:
        log(payload, lvl=hilight)
    receipt = client.publish(topic, payload)
    receipt.wait_for_publish()
    log("Delivered", lvl=info)


def ask_credentials():
    """Securely ask for user credentials.
    These can also be supplied as:

    * Arguments
    * Environment Variables (MN_USERNAME and MN_PASSWORD)
    * by configuration file
    """

    username = input("Enter MQTT username:")
    password = getpass("Enter MQTT password:")
    return username, password


@click.group(invoke_without_command=True)
@click.rich_config(help_config=click.RichHelpConfiguration(use_rich_markup=True))
@click.option(
    '-c', '--config',
    type=str,
    default=DEFAULT_CFG,
    callback=configure,
    is_eager=True,
    expose_value=False,
    help='Read option defaults from the specified INI file',
    show_default=True,
)
@click.option("--hostname", "-h", type=str, show_default=True, default=DEFAULT_SERVER, help="Broker hostname or ip")
@click.option("--port", "-p", type=int, show_default=True, default=DEFAULT_PORT, help="Broker TCP port")
@click.option("--topic", "-t", type=str, show_default=True, default=DEFAULT_TOPIC, help="Topic to work with")
@click.option("--login", "-l", is_flag=True, default=False,
              help="Ask for credentials (or supply as config, ENV or ARGs)")
@click.option("--username", "-u", type=str, default="", help="Supply username as argument")
@click.option("--password", "-p", type=str, default="", help="Supply password as argument (Unsafe!)")
@click.option("--verbosity", "-v", type=int, default=20)
@click.pass_context
def cli(ctx, hostname, port, topic, login, username, password, verbosity):
    """MQTTNotifier - Get notified via MQTT

    This tool displays configurable notifications by subscribing to a given
    topic on MQTT and waiting for json notification payload packets.

    Packets look like this example:

    \b
    {
       "title": "Your Broker",
       "message": "Hello, i'm a mqtt issued notification.",
       "timeout": 30,
       "app_icon": "actor",
       "app_name": "MQTT Notifier"
    }

    """

    set_verbosity(verbosity, verbosity)
    set_color(True)
    set_default_emitter("MQTT_NOTIFIER")

    log(f"MQTTNotifier! {version}", lvl=info)

    if ctx.invoked_subcommand is None:
        log("No subcommand given!", lvl=error)
        with click.Context(cli) as ctx:
            click.echo(ctx.get_help())
        sys.exit()

    ctx.ensure_object(dict)

    if login is True:
        username, password = ask_credentials()
    if 'MN_USERNAME' in os.environ or 'MN_PASSWORD' in os.environ:
        log("Using environment credentials", lvl=debug)
        username = os.environ.get('MN_USERNAME', username)
        password = os.environ.get('MN_PASSWORD', password)

    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    client = connect_mqtt(hostname, port, client_id, username, password)
    ctx.obj['client_id'] = client_id
    ctx.obj['client'] = client
    ctx.obj['topic'] = topic
    log("Client set up", lvl=debug)


@cli.command()
@click.pass_context
def launch(ctx):
    """Connect to MQTT and display notifications

    [i][yellow]Configure mqtt connection details as arguments before the launch command![/]"""
    client = ctx.obj['client']
    topic = ctx.obj['topic']

    subscribe(client, topic)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        log("Client stopped by keyboard interrupt, exiting.", lvl=info)
    except Exception as e:
        log("Client loop interrupted by unknown exception:", e, exc=True, lvl=error)

    client.disconnect()
    client.loop_stop()
    log("Client loop stopped, bye!", lvl=debug)


@cli.command()
@click.option("--show", "-s", is_flag=True, default=False, help="Show the payload to be transmitted")
@click.option("--title", "-t", type=str, default="MQTTNotifier Test", show_default=True,
              help="Notification window title")
@click.option("--message", "-m", type=str, default="Hello World!", show_default=True, help="Message body")
@click.option("--timeout", "-d", type=int, default=DEFAULT_TIMEOUT, show_default=True,
              help="Delay in seconds to hide notification")
@click.option("--app-name", "-a", type=str, default=DEFAULT_APPNAME, show_default=True,
              help="Specify a custom application title")
@click.option("--app-icon", "-i", type=str, default=DEFAULT_APPICON, show_default=True,
              help="Specify a notification icon (app or action icon)")
@click.pass_context
def test(ctx, **kwargs):
    """Send a test notification to MQTT\n\n

    [i][yellow]Configure mqtt connection details as arguments before the test command![/]
    """

    client = ctx.obj['client']
    topic = ctx.obj['topic']

    client.loop_start()
    publish_test_message(client, topic, **kwargs)
    client.loop_stop()
