from flask_restx import Resource
from flask import jsonify, request
from server import db
from models import ActivityModel


class Activities(Resource):
    def get(self):
        """
            Handle GET requests to retrieve all activities.

            This function retrieves all activity records from the database that are not marked as deleted. It serializes each activity's data into a JSON format and returns it. If an error occurs during the process, it returns a 500 Internal Server Error response with an error message.

            Returns:
                JSON: A response containing a list of serialized activities or an error message. Specifically:
                    - If the activities are successfully retrieved, returns a JSON array with serialized activity data.
                    - If there is a failure in fetching activities, returns a 500 Internal Server Error response with a message indicating the failure.

            HTTP Status Codes:
                - 200 OK: When the activities are successfully retrieved and the data is returned.
                - 500 Internal Server Error: When an error occurs during the retrieval or serialization of activities.

            Exceptions:
                - Handles any exceptions that occur during the process by rolling back the database session and returning an error response.
        """
        try:
            # Fetch all activities that are not deleted
            activities = ActivityModel.query.all()

            # Define a lambda function to serialize each activity
            serialize_activity = lambda activity: {
                'activityId': activity.activityid,
                'activityInfo': activity.activityinfo,
                'Date': activity.activitydate.strftime('%Y-%m-%d %H:%M:%S'),  # Formatting datetime
                'destination': activity.destination,
                'image': activity.image,
                'tags': activity.tags,  # Assuming this is a JSON-serializable field
                'destinationaddress': activity.destinationaddress,
                'userDistance': activity.userdistance,
                'availablePickUpLocation': activity.availablepickuplocation,  # Assuming this is a JSON-serializable field
                'ticketLink': activity.ticketlink
            }

            # Use map to apply serialization to each activity and convert to list
            activity_list = list(map(serialize_activity, activities))

            return jsonify(activity_list)
    
        except Exception as e:
            response = {"message": "Failed to fetch activities", "error": str(e)}
            return response, 500