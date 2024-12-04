import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.section import Section

"""
This Blueprint object is used to define APIs for the Section model.
- Blueprint is used to modularize application files.
- This Blueprint is registered to the Flask app in main.py.
"""
section_api = Blueprint('section_api', __name__, url_prefix='/api')

"""
The Api object is connected to the Blueprint object to define the API endpoints.
- The API object is used to add resources to the API.
- The objects added are mapped to code that contains the actions for the API.
- For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
"""
api = Api(section_api)

class SectionAPI:
    """
    Define the API CRUD endpoints for the Section model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new section 
    - get: read sections
    - put: update a section
    - delete: delete a section 
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new section.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Create a new section object using the data from the request
            section = Section(data['name'], data['theme'])
            # Save the section object using the Object Relational Mapper (ORM) method defined in the model
            section.create()
            # Convert Python object to JSON format
            json_ready = section.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)

        @token_required()
        def get(self):
            """
            Retrieve requested section.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Section data not found'}, 400
            if 'id' not in data:
                return {'message': 'Section ID not found'}, 400
            
            # Find and validate the section object
            section = Section.query.get(data['id'])
            if section is None:
                return {'message': 'Section not found'}, 404
           
            # Convert Python object to JSON format 
            json_ready = section.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)


        @token_required()
        def put(self):
            """
            Update a section.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Find the section to update
            section = Section.query.get(data['id'])
            if section is None:
                return {'message': 'Section not found'}, 404
            # Update the section object using the data from the request
            section._name = data['name']
            section._theme = data['theme']
            # Save the section object using the Object Relational Mapper (ORM) method defined in the model
            section.update()
            # Convert Python object to JSON format 
            json_ready = section.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)

        @token_required()
        def delete(self):
            """
            Delete a section.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Find the section to delete
            section = Section.query.get(data['id'])
            if section is None:
                return {'message': 'Section not found'}, 404
            # Delete the section object using the Object Relational Mapper (ORM) method defined in the model
            section.delete()
            # Return restful response message to the client
            return jsonify({'message': 'Section deleted'})

    class _BULK_CRUD(Resource):
        def post(self):
            """
            Handle bulk section creation by sending POST requests to the single section endpoint.
            """
            sections = request.get_json()

            if not isinstance(sections, list):
                return {'message': 'Expected a list of section data'}, 400

            # Initialize counters and results list
            results = {'errors': [], 'success_count': 0, 'error_count': 0}

            with current_app.test_client() as client:
                for section in sections:
                    # Simulate a POST request to the single section creation endpoint
                    response = client.post('/api/section', json=section)

                    if response.status_code == 200:
                        results['success_count'] += 1
                    else:
                        results['errors'].append(response.get_json())
                        results['error_count'] += 1

            # Return the results of the bulk creation process
            return jsonify(results)
        
        def get(self):
            """
            Retrieve all sections.
            """
            # Find all the sections
            sections = Section.query.all()
            # Converting Python objects to JSON format
            json_ready = []
            for section in sections:
                section_data = section.read()
                json_ready.append(section_data)
            # Return a JSON list of all the sections in restful response
            return jsonify(json_ready)

    """
    Map the _CRUD and _BULK_CRUD classes to the API endpoints for /section and /sections.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    - The _BULK_CRUD class defines the bulk operations for the API.
    """
    api.add_resource(_CRUD, '/section')
    api.add_resource(_BULK_CRUD, '/sections')