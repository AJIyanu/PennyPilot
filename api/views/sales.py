#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, request
from views import app_views
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.algorithms.sales import newSales as salesNew
from api.algorithms.sales import quickSales

@app_views.route('/sales/<stock_id>', methods=['POST'])
@jwt_required()
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
    if stock.stock_qty < details.get("qty", 1):
        return jsonify(error="Please add excess sales to quick stock'n'sell")
    status = None
    if "quicksales" in details:
        validate = ["qty", "sell", "cost"]
        for check in validate:
            if check not in details["quicksales"]:
                return jsonify(error=f"{check} is missing in quicksales parameters")
        status = quickSales(user_id=user_id,
                            product=stock.product_id,
                            name=stock.name,
                            **details.get("quicksales"))
        if status is None:
            return jsonify(error="New Sales not added")
    if details.get("qty", 0) == 0:
        return jsonify(status=f"quicks sales added with status, '{status}'")
    new = salesNew(user_id=user_id,
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
                (stock.cost_price * details.get("qty", 1)),
                "quicksales_status": status
                })
