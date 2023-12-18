import os

# 注意，celery4版本后，CELERY_BROKER_URL改为BROKER_URL

# https://docs.celeryproject.org/en/latest/userguide/configuration.html#broker-url
broker_url = os.getenv("CELERY_BROKER_URL", "")

# 任务发送完成是否需要确认，这一项对性能有一点影响
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#task-acks-late
task_acks_late = True

# 启动时，如果与 broker 的首次连接失败，Celery 是否应该尝试重新连接
broker_connection_retry_on_startup = True

# 连接broker的超时时间（秒）
# https://docs.celeryproject.org/en/stable/userguide/configuration.html#std-setting-broker_connection_timeout
broker_connection_timeout = 0.5
# broker_connection_max_retries = 1
# broker_pool_limit = 0
broker_transport_options = {
    "max_retries": 0,
    "interval_start": 0,
    "interval_step": 0.1,
    "interval_max": 0.1,
}

# 规定完成任务的时间 单位(秒) 否则执行该任务的worker将被杀死，任务移交给父进程
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#result-compression
task_time_limit = 60 * 16  # 15 分钟

# 软超时时间, task 可以 catch SoftTimeLimitExceeded 进行一些后续处理
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
task_soft_time_limit = 60 * 15

# 设置默认的队列名称，如果一个消息不符合其他的队列就会放在默认队列里面，如果什么都不设置的话，数据都会发送到默认的队列中
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#task-default-queue
task_default_queue = "default"

# 设置默认不存结果
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#task-ignore-result
task_ignore_result = True  # 需要返回结果的False


#  任务结果压缩方案选择，可以是zlib, bzip2，默认是发送没有压缩的数据
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#result-compression
result_compression = "zlib"

# 任务过期时间,celery任务执行结果的超时时间
# 任务结果过期时间,依赖(beat)
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#result-expires
result_expires = 60 * 60

# celery worker的并发数，默认是服务器的内核数目,也是命令行-c参数指定的数目
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-concurrency
worker_concurrency = 8
# celery worker 每次去rabbitmq预取任务的数量
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-prefetch-multiplier
worker_prefetch_multiplier = 10

# 每个worker执行了多少任务就会死掉，默认是无限的
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-max-tasks-per-child
worker_max_tasks_per_child = 200  # 每个进程最多执行200个任务后释放进程（再有任务，新建进程执行，解决内存泄漏）

# 限制 worker 每个进程最大内存数量 单位(KB) ,超出之后,完成任务之后,worker 将被替换
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-max-memory-per-child
worker_max_memory_per_child = 256 * 1000  # 256M


# https://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-log-format
worker_log_format = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"

# https://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-task-log-format
worker_task_log_format = (
    "[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s"
)

# 指定任务默认的序列化方法 4.0版本开始默认json,早期默认为pickle（可以传二进制对象
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#task-serializer
task_serializer = "pickle"

# https://docs.celeryproject.org/en/latest/userguide/configuration.html#result-serializer
result_serializer = "pickle"

# https://docs.celeryproject.org/en/latest/userguide/configuration.html#accept-content
accept_content = ["json", "pickle"]

# 是否将消息中的时间转成使用 UTC 时区,(3.0 开始默认启用)
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#enable-utc
enable_utc = False  # 禁用UTC时区

# 配置 celery 使用时区, 默认为 UTC
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#timezone
timezone = "Asia/Shanghai"  # 上海时区

# 默认为 true, 在 celery 处理逻辑中,最好在 after_setup_logger 信号中处理自定义日志
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-hijack-root-logger
worker_hijack_root_logger = True

# # beat 最多 sleep 60 秒就唤醒. 默认是 300秒.
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-max-loop-interval
# Celery Beat 配置
beat_max_loop_interval = 60
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-schedule
# celery beat 定时任务
# 配置项参考: https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#beat-entries
#
