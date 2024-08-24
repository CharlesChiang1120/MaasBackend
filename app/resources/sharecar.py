from flask_restx import Resource
from flask import jsonify, request
from server import db
from models import ShareCarEventModel


class ShareCar(Resource):
    def get(self):
        """
            Retrieve all ShareCarEvent records from the database.

            This method queries the database for all records in the `ShareCarEventModel` table. 
            It serializes the records into a JSON-serializable format and returns them in the response. 
            The serialization includes formatting of datetime fields and conversion of boolean values.

            Returns:
                Response: A Flask `jsonify` response containing a list of serialized ShareCarEvent records.
                If an error occurs during the process, a JSON response with an error message and status code 500 is returned.

            Example:
                HTTP GET request to /events
                Response:
                [
                    {
                        "id": "e6a31712-5d5e-4c7a-9b4b-1d2b5c82a1e0",
                        "carPreferences": {"type": "SUV", "color": "blue"},
                        "passengers": ["Alice", "Bob"],
                        "startTime": "2024-08-24 15:00:00",
                        "destination": "Downtown",
                        "departureLocations": ["Northside", "Eastside"],
                        "maxParticipants": [4],
                        "confirmed": true
                    },
                    ...
                ]

            Raises:
                Exception: If an error occurs while fetching or serializing the data, a JSON response with the error details is returned.
        """
        try:
            # Fetch all activities that are not deleted
            activities = ShareCarEventModel.query.all()

            # Define a lambda function to serialize each activity
            serialize_event = lambda event: {
                'id': event.id,
                'carPreferences': event.carpreferences,  # Assuming this is a JSON-serializable field
                'passengers': event.passengers,  # Assuming this is a JSON-serializable field
                'startTime': event.startTime.strftime('%Y-%m-%d %H:%M:%S') if event.startTime else None,  # Formatting datetime
                'destination': event.destination,
                'departureLocations': event.departurelocations,  # Assuming this is a JSON-serializable field
                'maxParticipants': event.maxparticipants,  # Assuming this is a JSON-serializable field
                'confirmed': bool(event.confirmed)  # Convert tinyint to boolean
            }

            # Use map to apply serialization to each activity and convert to list
            sharecar_list = list(map(serialize_event, activities))

            return jsonify(sharecar_list)
    
        except Exception as e:
            response = {"message": "Failed to fetch activities", "error": str(e)}
            return response, 500