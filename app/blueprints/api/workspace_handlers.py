from app.models.workspace.workspace import Workspace
from .blueprint import api
from flask import request, jsonify
from app.base import db
from app.helpers.id_helper import IdServer
from app.helpers.db_helper import *


@api.route('/workspace', methods=['POST'])
@mark_readwrite()
def create_workspace():
    data = request.json
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'message': 'Name is required'}), 400
    id = IdServer().new("wks")
    workspace = Workspace(id=id, name=name, description=description)

    db.session.add(workspace)
    db.session.commit()

    return jsonify({'message': 'Workspace created successfully', 'workspace': workspace.__repr__()}), 201


@api.route('/workspace/<string:id>', methods=['PUT'])
@mark_readwrite()
def update_workspace(id):
    workspace = Workspace.query.get(id)
    if not workspace:
        return jsonify({'message': 'Workspace not found'}), 404

    data = request.json
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'message': 'Name is required'}), 400

    workspace.name = name
    workspace.description = description
    db.session.commit()

    return jsonify({'message': 'Workspace updated successfully', 'workspace': workspace.__repr__()}), 200


@api.route('/workspace', methods=['GET'])
@mark_readonly()
def get_workspaces():
    workspaces = Workspace.query.all()
    return jsonify({'workspaces': [workspace.__repr__() for workspace in workspaces]}), 200


@api.route('/workspace/<string:id>', methods=['GET'])
@mark_readonly()
def get_workspace(id):
    workspace = Workspace.query.get(id)
    if not workspace:
        return jsonify({'message': 'Workspace not found'}), 404

    return jsonify({'workspace': workspace.__repr__()}), 200
