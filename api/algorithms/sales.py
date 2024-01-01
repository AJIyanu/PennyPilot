#!/usr/bin/env python3
"""process product"""

from objects.models.sales import Sales
from objects.models.stock import Stock

def newSales(**kwarg):
    """registers a new stock"""
    newSale = Sales(**kwarg)
    try:
        newSale.save()
    except Exception:
        return None
    return newSale.id


def quickSales(**kwargs):
    """to handle borrowed sales"""
    newQuickStock = Stock(user_id=kwargs.get("user_id"),
                          product_id=kwargs.get("product_id"),
                          cost=kwargs.get("cost"),
                          qty=kwargs.get("qty"),
                          name=kwargs.get("name"))
    try:
        newQuickStock.save()
    except Exception:
        return None
    newQuickSales = Sales(user_id=kwargs.get("user_id"),
                          product_id=kwargs.get("product_id"),
                          sell=kwargs.get("sell"),
                          qty=kwargs.get("qty"),
                          stock_id=newQuickStock.id,
                          name=kwargs.get("name"))
    try:
        newQuickSales.save()
    except Exception:
        return None
    return "done"
