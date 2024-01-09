# 项目初始化

1. 安装依赖库
    pip install -r requirements.txt
    pip freeze > requirements.txt
2. 安装依赖中间件
    1.数据库 pg 
    docker run --name my_postgres_container -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
    2.redis 缓存数据库
    docker run --name my_redis_container -p 6379:6379 -d redis
    3.es 数据库 和 kibana
    # 最新版本，需要使用https 集群模式，然后开启了认证，链接es时，需要使用安全模式，这里采用的是http 的 http_ca 证书，需要去容器把文件拷贝出来
    docker run -d --name kibana --link elasticsearch:elasticsearch -p 5601:5601 docker.elastic.co/kibana/kibana:8.11.3
    docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.11.3
    4.mq 中间件
    # 启动一个管理界面需要自己去容器内开启这个插件，rabbitmq-plugins enable rabbitmq_management
    docker run -d --name my_rabbitmq_container -p 5672:5672 -p 15672:15672 rabbitmq
2. 启动服务
    1.启动开发服务
    python server.py
    2.启动正式服务
    # mac-os High Sierra以上的操作系统对多线程的限制 
    # export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
    uwsgi --ini uwsgi.ini
    3.设置 flask db 迁移必须环境变量
    export FLASK_APP=server
    4.迁移数据库
    flask db init
    flask db migrate -m "" 修改模型类以后，需要执行这个更新数据库
    flask db upgrade
    5.格式化代码
    ./format.sh
    6.异步任务启动 worker 
    celery -A app.celery.celery_app:celery_app worker --loglevel=info
    :celery_app 是指定启动的时候 回去寻找你 实例化出来的 Celery 
    使用步骤，倒入对应的异步任务方法，然后就可以异步使用了 add.delay
    from app.celery.tasks.workspace_task import add
    7.调试 flask 代码
    export FLASK_APP=server
    flask shell
    8.全链路apm 监控追踪
    ELASTIC_APM
3.镜像打包
    1.docker build -t yzb_python_web .
    2.启动 docker run -p 5000:5000 yzb_python_web
