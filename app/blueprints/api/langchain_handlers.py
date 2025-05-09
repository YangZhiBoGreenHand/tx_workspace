from elasticsearch import Elasticsearch
from langchain.embeddings import OpenAIEmbeddings
from app.helpers.db_helper import mark_readwrite
from app.models.gpt.history import History

from app.models.gpt.topic import Topic
from .blueprint import api
from app.helpers.handler_context import HandlerContext as context
from langchain.chat_models import ChatOpenAI
from flask import request, jsonify
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationalRetrievalChain, LLMChain, ConversationChain
from app.base import app, db
from langchain.prompts import PromptTemplate
from langchain.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_community.llms.openai import OpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from langchain.vectorstores.elasticsearch import ElasticsearchStore
from langchain.retrievers import ChatGPTPluginRetriever


def track_tokens_usage(chain, chain_input):
    with get_openai_callback() as cb:
        result = chain(chain_input)
        print(f"Total tokens: {cb.total_tokens}")
        return result


@api.route('/text', methods=['POST'])
@mark_readwrite()
@context.custom_jwt_required
def get_text():
    data = request.json
    question = data.get('question')
    topic_id = data.get('topic_id')
    # 启动 OpenAI LLM
    llm = OpenAI(
        openai_api_key=app.config["OPENAI_API_KEY"], openai_proxy="http://127.0.0.1:7890")

    system_template = """你是一个 ai 聊天助手, 我们之间是有聊天记录的下面就是(--> 前面是提问，后面是回答):
        {chat_history}
        请你继续回答我的问题，我的问题是: {question} """

    prompt = PromptTemplate.from_template(system_template)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    history_entries = History.query.filter_by(
        topic_id=topic_id, user_id=request.current_user.id).order_by(History.created_at.desc()).limit(10).all()

    # 添加用户历史记录
    chat_history = reversed([(history_entry.question, history_entry.answer)
                             for history_entry in history_entries])
    chain_input = {"question": question,
                   "chat_history": '\n'.join([' --> '.join(t) for t in chat_history])}
    result = track_tokens_usage(chain, chain_input)
    # 创建用户主题，和 历史记录
    if data.get('first_question'):
        new_topic = Topic(name=question, user_id=request.current_user.id)
        db.session.add(new_topic)
        db.session.flush()
        topic_id = new_topic.id
    # 创建历史记录
    new_history = History(
        topic_id=topic_id,
        user_id=request.current_user.id,
        question=question,
        answer=result["text"]
    )

    db.session.add(new_history)
    db.session.commit()

    return context.success(data={"answer": result["text"], "topic_id": topic_id})


@api.route('/images', methods=['POST'])
@mark_readwrite()
@context.custom_jwt_required
def get_images():
    data = request.json
    question = data.get('question')
    llm = OpenAI(
        openai_api_key=app.config["OPENAI_API_KEY"], openai_proxy="http://127.0.0.1:7890")
    prompt = PromptTemplate(
        input_variables=["image_desc"],
        template="Generate a prompt to generate an image based on the following description: {image_desc}",
    )
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    image_url = DallEAPIWrapper().run(chain.run(question))

    return context.success(data={"image_url": image_url})


@api.route('/langchain_with_es_vector', methods=['POST'])
@mark_readwrite()
@context.custom_jwt_required
def use_langchain_with_es_vector():
    data = request.json
    question = data.get('question')
    topic_id = data.get('topic_id')
    # 启动 OpenAI LLM
    llm = OpenAI(
        openai_api_key=app.config["OPENAI_API_KEY"], openai_proxy="http://127.0.0.1:7890")

    # es 本地向量库的加载方式
    USERNAME = "elastic"
    PASSWORD = "elastic"
    ELATICSEARCH_ENDPOINT = "localhost:9200"
    ELASTCSEARCH_CERT_PATH = "/Users/yangzhibo/tx_workspace/http_ca.crt"
    url = f'https://{USERNAME}:{PASSWORD}@{ELATICSEARCH_ENDPOINT}'
    es_connection = Elasticsearch(
        url, ca_certs=ELASTCSEARCH_CERT_PATH, verify_certs=True)
    # loader = TextLoader("state_of_the_union.txt")
    # documents = loader.load()
    # text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    # docs = text_splitter.split_documents(documents)

    # db = ElasticsearchStore.from_documents(docs, embedding=OpenAIEmbeddings(),
    #                                        index_name="test_index",
    #                                        es_connection=es_connection)

    es_db = ElasticsearchStore(
        embedding=OpenAIEmbeddings(),
        index_name="test_index",
        es_connection=es_connection
    )
    # es_db.client.indices.refresh(index="test_index")
    # query = "阳志博是毕业于哪儿？"
    # results = db.similarity_search(query)
    # print(results)
    # 创建 retrieval chain 链

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm, verbose=True, retriever=es_db.as_retriever(), return_source_documents=True, max_tokens_limit=4097)

    history_entries = History.query.filter_by(
        topic_id=topic_id, user_id=request.current_user.id).order_by(History.created_at.desc()).limit(10).all()

    # 添加用户历史记录
    chat_history = reversed([(history_entry.question, history_entry.answer)
                             for history_entry in history_entries])

    chain_input = {"question": question, "chat_history": chat_history}
    result = track_tokens_usage(chain, chain_input)
    # 创建用户主题，和 历史记录
    if data.get('first_question'):
        new_topic = Topic(name=question, user_id=request.current_user.id)
        db.session.add(new_topic)
        db.session.flush()
        topic_id = new_topic.id
    # 创建历史记录
    new_history = History(
        topic_id=topic_id,
        user_id=request.current_user.id,
        question=question,
        answer=result["answer"]
    )

    db.session.add(new_history)
    db.session.commit()

    return context.success(data={"answer": result["answer"], "topic_id": topic_id})


@api.route('/langchain_with_faiss_vector', methods=['POST'])
@mark_readwrite()
@context.custom_jwt_required
def use_langchain_with_faiss_vector():
    data = request.json
    question = data.get('question')
    topic_id = data.get('topic_id')
    # 启动 OpenAI LLM
    llm = OpenAI(
        openai_api_key=app.config["OPENAI_API_KEY"], openai_proxy="http://127.0.0.1:7890")

    raw_documents = TextLoader('state_of_the_union.txt').load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_documents)
    retriever = FAISS.from_documents(
        documents, OpenAIEmbeddings()).as_retriever()
    # 创建 retrieval chain 链
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm, verbose=True, retriever=retriever, return_source_documents=True, max_tokens_limit=4097)
    history_entries = History.query.filter_by(
        topic_id=topic_id, user_id=request.current_user.id).order_by(History.created_at.desc()).limit(10).all()

    # 添加用户历史记录
    chat_history = reversed([(history_entry.question, history_entry.answer)
                             for history_entry in history_entries])
    chain_input = {"question": question, "chat_history": chat_history}
    result = track_tokens_usage(chain, chain_input)
    # 创建用户主题，和 历史记录
    if data.get('first_question'):
        new_topic = Topic(name=question, user_id=request.current_user.id)
        db.session.add(new_topic)
        db.session.flush()
        topic_id = new_topic.id
    # 创建历史记录
    new_history = History(
        topic_id=topic_id,
        user_id=request.current_user.id,
        question=question,
        answer=result["answer"]
    )

    db.session.add(new_history)
    db.session.commit()

    return context.success(data={"answer": result["answer"], "topic_id": topic_id})
