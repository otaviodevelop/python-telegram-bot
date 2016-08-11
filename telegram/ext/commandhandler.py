#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2016
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
""" This module contains the CommandHandler class """

from .handler import Handler
from telegram import Update
from telegram.utils.deprecate import deprecate


class CommandHandler(Handler):
    """
    Handler class to handle Telegram commands. Commands are Telegram messages
    that start with ``/``, optionally followed by an ``@`` and the bot's
    name and/or some additional text.

    Args:
        command (str): The name of the command this handler should listen for.
        callback (function): A function that takes ``bot, update`` as
            positional arguments. It will be called when the ``check_update``
            has determined that an update should be processed by this handler.
        allow_edited (Optional[bool]): If the handler should also accept edited messages.
            Default is ``False``
        pass_args (optional[bool]): If the handler should be passed the
            arguments passed to the command as a keyword argument called `
            ``args``. It will contain a list of strings, which is the text
            following the command split on spaces. Default is ``False``
        pass_update_queue (optional[bool]): If set to ``True``, a keyword argument called
            ``update_queue`` will be passed to the callback function. It will be the ``Queue``
            instance used by the ``Updater`` and ``Dispatcher`` that contains new updates which can
             be used to insert updates. Default is ``False``.
        pass_job_queue (optional[bool]): If set to ``True``, a keyword argument called
            ``job_queue`` will be passed to the callback function. It will be a ``JobQueue``
            instance created by the ``Updater`` which can be used to schedule new jobs.
            Default is ``False``.
    """

    def __init__(self,
                 command,
                 callback,
                 allow_edited=False,
                 pass_args=False,
                 pass_update_queue=False,
                 pass_job_queue=False):
        super(CommandHandler, self).__init__(callback,
                                             pass_update_queue=pass_update_queue,
                                             pass_job_queue=pass_job_queue)
        self.command = command
        self.allow_edited = allow_edited
        self.pass_args = pass_args

    def check_update(self, update):
        if (isinstance(update, Update)
                and (update.message or update.edited_message and self.allow_edited)):
            message = update.message or update.edited_message

            return (message.text and message.text.startswith('/')
                    and message.text[1:].split(' ')[0].split('@')[0] == self.command)

        else:
            return False

    def handle_update(self, update, dispatcher):
        optional_args = self.collect_optional_args(dispatcher)

        message = update.message or update.edited_message

        command = message.text[1:].split(' ')[0]
        if '@' in command:
            split_command = command.split('@')
            command, target_bot_name = split_command[0], split_command[1]
            calling_me = (target_bot_name.lower() == dispatcher.bot.username.lower())
            if not calling_me:
                return # don't reply, we aren't being talked to

        if self.pass_args:
            optional_args['args'] = message.text.split(' ')[1:]

        return self.callback(dispatcher.bot, update, **optional_args)

    # old non-PEP8 Handler methods
    m = "telegram.CommandHandler."
    checkUpdate = deprecate(check_update, m + "checkUpdate", m + "check_update")
    handleUpdate = deprecate(handle_update, m + "handleUpdate", m + "handle_update")
