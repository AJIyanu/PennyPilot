#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, request
from views import app_views
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.algorithms.sales import newSales

@app_views('/sales/<stock_id>', methods=['POST'])
@get_jwt_identity()
def newSales(stock_id):
    """adds new sales"""
    user_id = get_jwt_identity()
    details = request.json
    from objects import storage
    stock = storage.get("Stock", stock_id)
    if stock is None:
        abort(404)
    if stock.user_id != user_id:
        return jsonify(error="User not Authorized for stock")
    new = newSales(user_id=user_id,
                   stock_id=stock_id,
                   customer_id=details.get("customer_id"),
                   name=stock.name,
                   cost=stock.selling_price * details.get("qty", 1),
                   sell=details.get("sell", stock.selling_price),
                   qty=details.get("qty", 1))
    if new is None:
        return jsonify(error="New Sales not added")
    return jsonify({
                "status": f"{stock.name} has been sold for {details.get('sell')} successfully",
                "sales_id": new,
                "profit": (details.get("sell", stock.selling_price * details.get("qty", 1))) -
                (stock.cost_price * details.get("qty", 1))
                })
