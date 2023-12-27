#!/usr/bin/python3
"""
initialize the models package
"""

from objects.storage.sqlstorage import MySqlVault

storage = MySqlVault()
storage.reload()
