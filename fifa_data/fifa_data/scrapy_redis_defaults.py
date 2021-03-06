from rejson import Client


# For standalone use.
DUPEFILTER_KEY = 'dupefilter:%(timestamp)s'

PIPELINE_KEY = '%(spider)s:%(url)s:items'

REDIS_CLS = Client
REDIS_ENCODING = 'utf-8'
# Sane connection defaults.
REDIS_PARAMS = {
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
    'retry_on_timeout': True,
    'encoding': REDIS_ENCODING,
}

SCHEDULER_QUEUE_KEY = 'club_queue'
SCHEDULER_QUEUE_CLASS = 'fifa_data.scrapy_redis_queue.FifoQueue'
SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'
SCHEDULER_DUPEFILTER_CLASS = 'fifa_data.scrapy_redis_dupefilter.RFPDupeFilter'

START_URLS_KEY = 'club_urls'
START_URLS_AS_SET = True
