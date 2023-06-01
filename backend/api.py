import os
import collections
# import sys
# sys.path.append(r'C:/Users/Destiny Otto/Coding World/Full_Stack_Development_Python/Coffee_Shop_App/backend')

from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

# # from .database.models import db_drop_and_create_all, setup_db, Drink
# from .database.models import db_drop_and_create_all, setup_db, Drink
# from .auth.auth import AuthError, requires_auth

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth


app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
with app.app_context():
    db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    selection = Drink.query.all()
    # if len(selection) == 0:
    #     abort(404)
    drinks = [drink.short() for drink in  selection]
     
    return jsonify({
        "success": True,
        "drinks": drinks
    }),200

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        with app.app_context():
            selection = Drink.query.all()
            if len(selection) == 0:
                abort(404)
            drinks = [drink.long() for drink in selection]
            
            return jsonify({
                "success": True,
                "drinks": drinks
            }),200
    except Exception as e:
        print(e)
        abort(500)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(payload):
    data = request.get_json()
    title = data.get('title')
    recipe = data.get('recipe')

    if not all([title, recipe]):
        abort(400, description="missing required fields")
    try:
        with app.app_context():
            new_drink = Drink(title=title, recipe=json.dumps(recipe))
            new_drink.insert()
            new_drink = new_drink.long()

        return jsonify({
            "success": True,
            "drinks": [new_drink]
        }), 200

    except Exception as e:
        print(f"Error creating drink: {e}")
        abort(500, description="Error creating new drink")



'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(payload, id):
    data = request.get_json()
    title = data.get('title')
    recipe = data.get('recipe')
    
    try:
        drink = Drink.query.get(id)
    
        if not drink:
            abort(404, description='drink not found')
        if title is not None:
            drink.title = title
        if recipe is not None:
            drink.recipe = json.dumps(recipe)
            
        with app.app_context():
            drink.update()
            
        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        }), 200
            
    except Exception as e:
        print(f"Error creating drink: {e}")
        abort(500, description="Error creating new drink") 

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, id):
    try:
        with app.app_context():
            drink = Drink.query.get(id)
            if not drink:
                abort(404, description="drink not found")
            drink.delete()
              
        return jsonify({
            "success": True,
            "delete": id
        }), 200
            
    except Exception as e:
        print(f"Error deleting drink: {e}")
        abort(422, description="Cannot delete drink") 


# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(500)
def internal_server_error(error):
    response = jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500
'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
# Error handler for AuthError
@app.errorhandler(AuthError)
def handle_auth_error(error):
    response = jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error['description']
    })
    response.status_code = error.status_code
    return response


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403
    
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401
    
