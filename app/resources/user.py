from flask_restx import Resource
from flask import jsonify, request
from server import db
from models import UserModel


class UserGet(Resource):
    def get(self, name):
        """
            Handle GET requests to retrieve a user by their name.

            This function retrieves a user record from the database based on the provided name. It performs a lookup and returns the user data if found. If the user is not found, it returns a 404 Not Found response.

            Parameters:
                name (str): The name of the user to retrieve.

            Returns:
                JSON: A response containing the user data or an error message. Specifically:
                    - If the user is found, returns a JSON object with the user's serialized data.
                    - If the user is not found, returns a 404 Not Found response with a message indicating that the user was not found.

            HTTP Status Codes:
                - 200 OK: When the user is found and the data is successfully retrieved.
                - 404 Not Found: When no user with the specified name exists in the database.

            Exceptions:
                - This function does not handle specific exceptions, but any issues with database access or serialization would result in an error handled by Flask's global error handling mechanisms.
        """
        user = UserModel.query.filter_by(name=name).first()
        if not user:
            response = {"message": "User not found"}
            return response, 404

        return jsonify(user.serialize())

class User(Resource):
    def post(self):
        """
            Handle POST requests to create a new user in the database.

            This function expects a JSON payload with required fields to create a new user. It performs validation to ensure all required fields are present, then attempts to add the new user to the database.

            Steps:
            1. Retrieve the JSON data from the request body.
            2. Define the required fields that must be present in the request payload.
            3. Check if any of the required fields are missing.
            4. If there are missing fields, return a 400 Bad Request response with details about the missing fields.
            5. If all required fields are present, attempt to create a new user record.
            6. Add the new user to the database and commit the transaction.
            7. If successful, return a 201 Created response with a success message and the serialized user data.
            8. In case of an error, roll back the transaction and return a 500 Internal Server Error response with an error message.

            Returns:
                JSON: A response indicating the result of the create operation, which includes:
                    - message (str): Description of the result (success or failure).
                    - user (dict, optional): Serialized user data if the operation is successful.

            HTTP Status Codes:
                - 201 Created: When the user is successfully created.
                - 400 Bad Request: When required fields are missing from the request.
                - 500 Internal Server Error: When an exception occurs during the creation process.

            Exceptions:
                - Catches exceptions that occur during the database operation, rolls back the transaction, and returns an error message.
        """

        data = request.json
    
        # Define required fields
        required_fields = [
            'name', 
            'gender', 
            'mail', 
            'phonenumber'
        ]
        
        # Check for missing required fields
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {"message": "Missing required fields", "missing": missing_fields}, 400

        try:
            new_user = UserModel(
                name=data['name'],
                gender=data['gender'],
                mail=data['mail'],
                passengercustom_1=data['passengercustom_1'],
                passengercustom_2=data['passengercustom_2'],
                passengercustom_3=data['passengercustom_3'],
                payment=data['payment'],
                deleted=0,
                phonenumber=data['phonenumber'],
                pickuplocation=data['pickuplocation']
            )

            db.session.add(new_user)
            db.session.commit()

            response = {
                "message": "User added successfully",
                "user": new_user.serialize()
            }

            return response, 201
        
        except Exception as e:
            db.session.rollback()
            response = {
                "message": "Failed to add user",
                "error": str(e)
            }

            return response, 500
        
    def patch(self):
        """
            Handle PATCH requests to update user information in the database.

            This function updates user fields based on the provided JSON payload. It expects a JSON object with at least a `name` field to identify the user and optionally other fields to update.

            Steps:
            1. Retrieve the JSON data from the request body.
            2. Find the user in the database using the provided `name`.
            3. If the user is not found, return a 404 Not Found response.
            4. Update the user fields with the provided data if they are present in the request.
            5. Commit the changes to the database.
            6. If successful, return a 200 OK response with a success message.
            7. In case of an error, roll back the transaction and return a 500 Internal Server Error response with an error message.

            Returns:
                JSON: A response indicating the result of the update operation, which includes:
                    - message (str): Description of the result (success or failure).

            HTTP Status Codes:
                - 200 OK: When the user is successfully updated.
                - 404 Not Found: When the user with the specified name is not found.
                - 500 Internal Server Error: When an exception occurs during the update process.

            Exceptions:
                - Catches exceptions that occur during the update operation, rolls back the transaction, and returns an error message.
        """
        # Get JSON data from the request body
        data = request.get_json()

        # Find the user by name and id
        user = UserModel.query.filter_by(name=data['name']).first()
        if not user:
            response = {"message": "User not found"}
            return response, 404

        # Update the user fields with the provided data
        if 'name' in data:
            user.name = data['name']
        if 'gender' in data:
            user.gender = data['gender']
        if 'mail' in data:
            user.mail = data['mail']
        if 'passengercustom_1' in data:
            user.passengercustom_1 = data['passengercustom_1']
        if 'passengercustom_2' in data:
            user.passengercustom_2 = data['passengercustom_2']
        if 'passengercustom_3' in data:
            user.passengercustom_3 = data['passengercustom_3']
        if 'payment' in data:
            user.payment = data['payment']
        if 'phonenumber' in data:
            user.phonenumber = data['phonenumber']
        if 'pickuplocation' in data:
            user.pickuplocation = data['pickuplocation']

        try:
            # Commit the changes to the database
            db.session.commit()
            response = {"message": "User updated successfully"}
            return response, 200
        
        except Exception as e:
            # Rollback the session in case of error
            db.session.rollback()
            response = {
                "message": "Failed to updated user",
                "error": str(e)
            }

            return response, 500
    
    def delete(self):
        """
            Handle DELETE requests to remove a user from the database.

            This function deletes a user identified by their name. It expects a JSON payload with the user's name.

            Steps:
            1. Retrieve the JSON data from the request body.
            2. Find the user in the database by their name.
            3. If the user is not found, return a 404 Not Found response.
            4. Attempt to delete the user from the database.
            5. Commit the changes to the database.
            6. If successful, return a 200 OK response with a success message.
            7. In case of an error, roll back the transaction and return a 500 Internal Server Error response with an error message.

            Returns:
                JSON: A response indicating the result of the delete operation, which includes:
                    - message (str): Description of the result (success or failure).

            HTTP Status Codes:
                - 200 OK: When the user is successfully deleted.
                - 404 Not Found: When the user with the specified name is not found.
                - 500 Internal Server Error: When an exception occurs during the delete process.

            Exceptions:
                - Catches exceptions that occur during the delete operation, rolls back the transaction, and returns an error message.
        """
        data = request.get_json()
        # Find the user by name and id
        user = UserModel.query.filter_by(name=data['name']).first()
        if not user:
            response = {"message": "User not found"}
            return response, 404
        
        try:
            # Delete the user from the database
            db.session.delete(user)
            db.session.commit()

            return jsonify({"message": "User deleted successfully"})
        except Exception as e:
            # Rollback the session in case of error
            db.session.rollback()
            response = {
                "message": "Failed to delete user",
                "error": str(e)
            }

            return response, 500

class Users(Resource):
    def get(self):
        """
            Handle GET requests to retrieve a list of users.

            This function queries the database for all users who have not been marked as deleted.
            It serializes the user data into a format suitable for JSON output and returns it.
            
            Steps:
            1. Query the database to filter out users where 'deleted' is not True.
            2. Serialize the user data into a dictionary format using a lambda function.
            3. Convert the serialized user data into a list.
            4. Return the list of users as a JSON response.

            Returns:
                JSON: A list of dictionaries representing users, each containing the following fields:
                    - name (str): The name of the user.
                    - gender (str): The gender of the user.
                    - mail (str): The email address of the user.
                    - passengercustom_1 (str): Custom passenger field 1.
                    - passengercustom_2 (str): Custom passenger field 2.
                    - passengercustom_3 (str): Custom passenger field 3.
                    - payment (int): Payment status.
                    - phonenumber (str): Phone number of the user.
                    - pickuplocation (str): Pickup location of the user.

            HTTP Status Code:
                - 200 OK: When the request is successful and user data is returned.
                - 500 Internal Server Error: When an exception occurs while fetching user data.

            Exceptions:
                - Catches all exceptions and returns a JSON response with an error message and details.
        """
        try:
            users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
            # Define a lambda function to serialize each user
            serialize_user = lambda user: {
                'name': user.name,
                'gender': user.gender,
                'mail': user.mail,
                'passengercustom_1': user.passengercustom_1,
                'passengercustom_2': user.passengercustom_2,
                'passengercustom_3': user.passengercustom_3,
                'payment': user.payment,
                'phonenumber': user.phonenumber,
                'pickuplocation': user.pickuplocation
            }
            user_list = list(map(serialize_user, users))
            return jsonify(user_list)
        
        except Exception as e:
            response = {
                "message": "Failed to get user",
                "error": str(e)
            }

            return response, 500
        
class UserPickupLocation(Resource):
    def patch(self):
        """
            Handle PATCH requests to update a user's pickup location.

            This function updates the 'pickuplocation' field for a user identified by their name.
            It expects a JSON payload with the new pickup location and the user's name.

            Steps:
            1. Retrieve the JSON data from the request body.
            2. Check if 'pickuplocation' is present in the request data.
            3. Fetch the user from the database by their name.
            4. If the user is not found, return a 404 Not Found response.
            5. Update the user's 'pickuplocation' with the new value.
            6. Commit the changes to the database.
            7. If successful, return a 200 OK response with a success message.
            8. In case of an error, roll back the transaction and return a 500 Internal Server Error response with an error message.

            Returns:
                JSON: A response indicating the result of the update operation, which includes:
                    - message (str): Description of the result (success or failure).

            HTTP Status Codes:
                - 200 OK: When the pickup location is updated successfully.
                - 400 Bad Request: When the 'pickuplocation' field is missing in the request.
                - 404 Not Found: When the user with the specified name is not found.
                - 500 Internal Server Error: When an exception occurs during the update process.

            Exceptions:
                - Catches exceptions that occur during the update operation, rolls back the transaction, and returns an error message.
        """
        data = request.get_json()
    
        if 'pickuplocation' not in data:
            response = {"message": "Missing 'pickuplocation' field"}
            return response, 400
        
        user = UserModel.query.filter_by(name=data['name']).first()
        
        if not user:
            response = {"message": "User not found"}
            return response, 404

        try:
            user.pickuplocation = data['pickuplocation']
            db.session.commit()
            response = {"message": "User updated successfully"}
            return response, 200
        
        except Exception as e:
            db.session.rollback()
            response = {"message": "Failed to update user", "error": str(e)}
            return response, 500