import datetime
from fifa_data.mongodb_addr import host, port


def sofifa_settings(database, name, proxies, user_agent, collection, validator,
                    timeout):

    settings = {

        # DATABASE SETTINGS
        'MONGO_DB': f'{database}',
        'MONGO_URI': f'mongodb://{host}:{port}',
        'COLLECTION_NAME': f'{collection}',

        # SPIDER CHECKPOINTS
        'JOBDIR': f'pause_resume/{name}',

        # SPIDER LOGGING
        'LOG_ENABLED': True,
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': f'{name}_log_{datetime.date.today()}.txt',

        # EXTENSION ACTIVATION
        'SPIDERMON_ENABLED': True,
        'PROXY_POOL_ENABLED': True,
        'EXTENSIONS': {
            'fifa_data.test_extension.CustomStats': 600,
            'spidermon.contrib.scrapy.extensions.Spidermon': 510,
            'scrapy.extensions.closespider.CloeseSpider': 400,
        },

        # BAN PREVENTION
        'ROTATING_PROXY_LIST': proxies,
        'USER_AGENTS': user_agent,

        # MISC. SETTINGS
        'HTTPCACHE_ENABLED': False,
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_TIMEOUT': 30,
        'CLOSESPIDER_TIMEOUT': timeout,

        # PIPELINES, MIDDLEWARES, AND EXTENSIONS
        'ITEM_PIPELINES': {
            'fifa_data.pipelines.MongoDBPipeline': 300,
            'fifa_data.pipelines.SpiderStats': 301,
            'fifa_data.pipelines.ProxyPipeline': 302,
            'spidermon.contrib.scrapy.pipelines.ItemValidationPipeline': 800,
        },

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.\
            UserAgentsMiddleware': 500,
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620
        },

        'SPIDERMON_SPIDER_CLOSE_MONITORS': (
            'fifa_data.monitors.SpiderCloseMonitorSuite',
        ),

        'SPIDERMON_VALIDATION_MODELS': (
            f'fifa_data.validators.{validator}',
        ),

        'SPIDERMON_PERIODIC_MONITORS': {
            'fifa_data.monitors.PeriodicMonitorSuite': 60,
        },

        # TODO: integrate expected finish reasons into settings: currently defined in monitors.
        # 'SPIDERMON_EXPECTED_FINISH_REASONS': ['finished', ]
    }

    return settings
