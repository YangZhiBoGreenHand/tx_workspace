from sqlalchemy import or_
from app.models.gpt.history import History
from app.models.gpt.topic import Topic
from .blueprint import api
from flask import request, jsonify
from app.base import db
from app.helpers.id_helper import IdServer
from app.helpers.db_helper import *
from app.helpers.handler_context import HandlerContext as context
from elasticsearch import Elasticsearch
from langchain.vectorstores.elasticsearch import ElasticsearchStore
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter


@api.route('/topics', methods=['GET'])
@mark_readonly()
@context.custom_jwt_required
def get_topics():
    user_id = request.current_user.id
    topics = Topic.query.filter_by(user_id=user_id).all()
    topic_ids = [topic.id for topic in topics]
    history_entries = History.query.filter(
        History.topic_id.in_(topic_ids), History.user_id == user_id).order_by(History.created_at).all()

    topic_history_map = {}
    for entry in history_entries:
        history_list = dict.get(topic_history_map, entry.topic_id, [])
        history_list.append({
            'id': entry.id,
            'topic_id': entry.topic_id,
            'user_id': entry.user_id,
            'question': entry.question,
            'answer': entry.answer,
            'created_at': entry.created_at,
            'updated_at': entry.updated_at
        })
        topic_history_map[entry.topic_id] = history_list

    topic_list = []
    for topic in topics:
        topic_list.append({
            'id': topic.id,
            'name': topic.name,
            'user_id': topic.user_id,
            'created_at': topic.created_at,
            'updated_at': topic.updated_at,
            'history_list': topic_history_map[topic.id]
        })
    # 使用 SQL 连接一次性获取主题和历史记录
    # topics_and_history = db.session.query(
    #     Topic.id,
    #     Topic.name,
    #     Topic.user_id,
    #     Topic.created_at,
    #     Topic.updated_at,
    #     History.id,
    #     History.topic_id,
    #     History.user_id,
    #     History.question,
    #     History.answer,
    #     History.created_at.label("history_created_at"),
    #     History.updated_at.label("history_updated_at")
    # ).join(History, History.topic_id == Topic.id).filter(
    #     Topic.user_id == user_id
    # ).order_by(History.created_at).all()

    return context.success(data={"topic_list": topic_list})
