#!/usr/bin/env python3
"""process product"""

from objects.models.stock import Stock

def newStock(**kwargs):
    """registers a new stock"""
    newStock = Stock(**kwargs)
    try:
        newStock.save()
    except Exception:
        return None
    return newStock.id
