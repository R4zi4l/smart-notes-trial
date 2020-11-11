#!/usr/bin/env python3

import sys
import asyncio

from tornado.ioloop import IOLoop


if sys.platform.startswith("win32"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # TODO: show warning for setting asyncio event loop policy

from .app import run
IOLoop.current().spawn_callback(run)

try:
    IOLoop.current().start()
except KeyboardInterrupt:
    IOLoop.instance().stop() # TODO: show warning for KeyboardInterrupt exception
