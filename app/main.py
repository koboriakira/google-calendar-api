import logging

logger = logging.Logger(name=__name__)

def handler(event, context):
    logger.info(event)
    return {
        # 'statusCode': 200,
        # 'body': 'Hello World!'
        'status': "ok",
    }
