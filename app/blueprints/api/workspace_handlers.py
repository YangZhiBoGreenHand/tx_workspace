from app.models.workspace.workspace import Workspace
from .blueprint import api
from flask import request, jsonify
from app.base import db
from app.helpers.id_helper import IdServer
from app.helpers.db_helper import *
from app.helpers.handler_context import HandlerContext as context


@api.route('/workspaces', methods=['POST'])
@mark_readwrite()
@context.custom_jwt_required
def create_workspace():
    data = request.json
    name = data.get('name')
    description = data.get('description')

    if not name:
        return context.success({}, 'Name is required', 400)
    id = IdServer().new("wks")
    workspace = Workspace(id=id, name=name, description=description)

    db.session.add(workspace)
    db.session.commit()
    return context.success(workspace, 'Workspace created successfully', 201)


@api.route('/workspaces/<string:id>', methods=['PUT'])
@mark_readwrite()
@context.custom_jwt_required
def update_workspace(id):
    workspace = Workspace.query.get(id)
    if not workspace:
        return context.success({}, 'Workspace not found', 404)

    data = request.json
    name = data.get('name')
    description = data.get('description')

    if not name:
        return context.success({}, 'Name is required', 400)
    workspace.name = name
    workspace.description = description
    db.session.commit()

    return context.success(
        data=workspace,
        message='Workspace updated successfully')


@api.route('/workspaces', methods=['GET'])
@mark_readonly()
# @context.custom_jwt_required
def get_workspaces():
    workspaces = Workspace.query.all()
    return context.success(data=workspaces)


@api.route('/workspaces/<string:id>', methods=['GET'])
@mark_readonly()
@context.custom_jwt_required
def get_workspace(id):
    workspace = Workspace.query.get(id)
    if not workspace:
        return context.success({}, 'Workspace not found', 404)

    return context.success(data=workspace)
