#!/usr/bin/env python3

"""
Entrypoint for directly running module
"""

from .app import create_app

if __name__ == "__main__":
    create_app().run()
