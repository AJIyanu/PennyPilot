#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, request
from views import app_views
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.algorithms.product import addNew



@app_views.route("/newproduct", methods=["POST"])
@jwt_required()
def add_new():
    """adds new product for user"""
    user_id = get_jwt_identity()
    details = request.json
    new = addNew(user_id, **details)
    if new is None:
        return jsonify(error="Product not added"), 400
    return jsonify({ "status": f"{details.get('name')} has been added succesfully",
                    "userId": new }), 200

@app_views.route("/product/<id>", methods=["GET"])
@jwt_required()
def findProduct(id):
    """returns the json rep of product"""
    from objects import storage
    product = storage.get("Product", id)
    if product is None:
        return jsonify(error="Product not registered")
    if product.isActive is False:
        return jsonify(error="Product is temporarily unvaialable")
    user_id = get_jwt_identity()
    if product.user_id != user_id:
        return jsonify(error="Unauthorized product")
    return jsonify(product.to_dict())

@app_views.route("product/<id>/toggle", methods=["GET"])
@jwt_required()
def toggleProduct(id):
    """removes or readd product"""
    from objects import storage
    product = storage.get("Product", id)
    if product is None:
        return jsonify(error="Product not registered")
    user_id = get_jwt_identity()
    if product.user_id != user_id:
        return jsonify(error="Unauthorized product")
    product.toggleProductActive()
    return jsonify(status=f"{product.name} is now {product.isActive}")
