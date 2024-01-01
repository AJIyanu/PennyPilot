#!/usr/bin/env python3
"""process product"""

from objects.models.sales import Sales

def newSales(**kwarg):
    """registers a new stock"""
    newSale = Sales(**kwarg)
    try:
        newSale.save()
    except Exception:
        return None
    return newSale.id
