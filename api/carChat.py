import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.carChat import CarChat
from model.user import User
from model.section import Section

# """
# This Blueprint object is used to define APIs for the Group model.
# - Blueprint is used to modularize application files.
# - This Blueprint is registered to the Flask app in main.py.
# """
# group_api = Blueprint('group_api', __name__, url_prefix='/api')
car_chat_api = Blueprint('car_chat_api', __name__, url_prefix='/api')

# """
# The Api object is connected to the Blueprint object to define the API endpoints.
# - The API object is used to add resources to the API.
# - The objects added are mapped to code that contains the actions for the API.
# - For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
# """
# api = Api(group_api)
api = Api(car_chat_api)

class GroupAPI:
    """
    Define the API CRUD endpoints for the Group model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new group
    - get: read groups
    - put: update a group
    - delete: delete a group
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new group.
            """
            print(request.get_json())
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            print(data)
            # Create a new group object using the data from the request
            chat = CarChat(data['message'], current_user.id)
            # Save the chat object using the Object Relational Mapper (ORM) method defined in the model
            chat.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(chat.read())

        def get(self):

            chats = CarChat.query.all()
            allChats = []
            for i in range(len(chats)):
                allChats.append(chats[i].read())

            # Return a JSON restful response to the client
            return jsonify(allChats)

        
#     class _BULK_CRUD(Resource):
#         def post(self):
#             """
#             Handle bulk group creation by sending POST requests to the single group endpoint.
#             """
#             groups = request.get_json()

#             if not isinstance(groups, list):
#                 return {'message': 'Expected a list of group data'}, 400

#             results = {'errors': [], 'success_count': 0, 'error_count': 0}

#             with current_app.test_client() as client:
#                 for group in groups:
#                     # Simulate a POST request to the single group creation endpoint
#                     response = client.post('/api/group', json=group)

#                     if response.status_code == 200:
#                         results['success_count'] += 1
#                     else:
#                         results['errors'].append(response.get_json())
#                         results['error_count'] += 1

#             # Return the results of the bulk creation process
#             return jsonify(results)
        
#         def get(self):
#             """
#             Retrieve all groups.
#             """
#             # Find all the groups
#             groups = Group.query.all()
#             # Prepare a JSON list of all the groups, using list comprehension
#             json_ready = []
#             for group in groups:
#                 group_data = group.read()
#                 json_ready.append(group_data)
#             # Return a JSON list, converting Python dictionaries to JSON format
#             return jsonify(json_ready)

#     class _MODERATOR(Resource):
#         @token_required()
#         def post(self):
#             """
#             Add a moderator to a group.
#             """
#             # Obtain the request data sent by the RESTful client API
#             data = request.get_json()
#             # Find the group to update
#             group = Group.query.get(data['group_id'])
#             if group is None:
#                 return {'message': 'Group not found'}, 404
#             # Find the user to add as a moderator
#             user = User.query.get(data['user_id'])
#             if user is None:
#                 return {'message': 'User not found'}, 404
#             # Add the user as a moderator
#             group.moderators.append(user)
#             # Save the group object using the Object Relational Mapper (ORM) method defined in the model
#             group.update()
#             # Return response to the client in JSON format, converting Python dictionaries to JSON format
#             return jsonify(group.read())

#         @token_required()
#         def delete(self):
#             """
#             Remove a moderator from a group.
#             """
#             # Obtain the request data sent by the RESTful client API
#             data = request.get_json()
#             # Find the group to update
#             group = Group.query.get(data['group_id'])
#             if group is None:
#                 return {'message': 'Group not found'}, 404
#             # Find the user to remove as a moderator
#             user = User.query.get(data['user_id'])
#             if user is None:
#                 return {'message': 'User not found'}, 404
#             # Remove the user as a moderator
#             group.moderators.remove(user)
#             # Save the group object using the Object Relational Mapper (ORM) method defined in the model
#             group.update()
#             # Return response to the client in JSON format, converting Python dictionaries to JSON format
#             return jsonify(group.read())

#     class _BULK_FILTER(Resource):
#         @token_required()
#         def post(self):
#             """
#             Retrieve all groups under a section by section name.
#             """
#             # Obtain and validate the request data sent by the RESTful client API
#             data = request.get_json()
#             if data is None:
#                 return {'message': 'Section data not found'}, 400
#             if 'section_name' not in data:
#                 return {'message': 'Section name not found'}, 400
            
#             # Find the section by name
#             section = Section.query.filter_by(_name=data['section_name']).first()
#             if section is None:
#                 return {'message': 'Section not found'}, 404
            
#             # Find all groups under the section
#             groups = Group.query.filter_by(_section_id=section.id).all()
#             # Prepare a JSON list of all the groups, using list comprehension
#             json_ready = [group.read() for group in groups]
#             # Return a JSON list, converting Python dictionaries to JSON format
#             return jsonify(json_ready)

#     class _FILTER(Resource):
#         @token_required()
#         def post(self):
#             """
#             Retrieve a single group by group name.
#             """
#             # Obtain and validate the request data sent by the RESTful client API
#             data = request.get_json()
#             if data is None:
#                 return {'message': 'Group data not found'}, 400
#             if 'group_name' not in data:
#                 return {'message': 'Group name not found'}, 400
            
#             # Find the group by name
#             group = Group.query.filter_by(_name=data['group_name']).first()
#             if group is None:
#                 return {'message': 'Group not found'}, 404
            
#             # Convert Python object to JSON format 
#             json_ready = group.read()
#             # Return a JSON restful response to the client
#             return jsonify(json_ready)

#     """
#     Map the _CRUD, _BULK_CRUD, _BULK_FILTER, and _FILTER classes to the API endpoints for /group, /groups, /groups/filter, and /group/filter.
#     - The API resource class inherits from flask_restful.Resource.
#     - The _CRUD class defines the HTTP methods for the API.
#     - The _BULK_CRUD class defines the bulk operations for the API.
#     - The _BULK_FILTER class defines the endpoints for filtering groups by section name.
#     - The _FILTER class defines the endpoints for filtering a specific group by group name.
#     """
    api.add_resource(_CRUD, '/car_chat')
#     api.add_resource(_BULK_CRUD, '/groups')
#     api.add_resource(_BULK_FILTER, '/groups/filter')
#     api.add_resource(_FILTER, '/group/filter')