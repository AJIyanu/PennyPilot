#!/usr/bin/env python3
"""process product"""

from objects.models.sales import Sales

def newSales(**kwargs):
    """registers a new stock"""
    newSale = Sales()(**kwargs)
    try:
        newSale.save()
    except Exception:
        return None
    return newSale.id
