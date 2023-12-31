#!/usr/bin/env python3
"""process product"""


from objects.models.products import Product

def addNew(userId, **details):
    """saves a new product"""
    new = Product(user_id=userId, **details)
    try:
        new.save()
    except Exception:
        return None
    return new.id
