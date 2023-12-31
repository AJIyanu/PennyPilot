#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, request
from views import app_views
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.algorithms.stock import newStock

@app_views.route("/newstock/<id>", methods=['POST'])
@jwt_required()
def addNewStock(id):
    """adds new stock to market"""
    user_id = get_jwt_identity()
    details = request.json
    from objects import storage
    product = storage.get("Product", id)
    if product is None:
        abort(404)
    if product.user_id != user_id:
        return jsonify(error="User not authorized to use product")
    new = newStock(user_id=user_id,
                   name=product.name,
                   sell=details.get("sell", product.selling_price),
                   cost=details.get("cost", product.cost_price),
                   product=product.id,
                   qty=details.get("qty", 1))
    if new is None:
        return jsonify(error="New Stock is not added"), 400
    return jsonify({
                "status": f"{new.name} has been added successfully",
                "stock_id": new,
                "qauantity": details.get("qty", 1)
                    })

@app_views.route("/stock/<id>", methods=["GET"])
@jwt_required()
def stockInfo(id):
    """returns json of stock infomation"""
    user_id = get_jwt_identity()
    from objects import storage
    stock = storage.get("Stock", id)
    if stock is None:
        abort(404)
    if user_id != stock.user_id:
        return jsonify(error="User not authorized on stock")
    return jsonify(stock.to_dict())
