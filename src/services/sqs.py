from  utils.logger import logger
import boto3
from  config import APP_CONFIG
import json

region_name = 'us-east-1'
sqs = boto3.resource("sqs",region_name=region_name)

def consumer(process_message_fn):
    print("data_pip_sqs_consumer_queue_name : "+APP_CONFIG.data_pip_sqs_consumer_queue_name)
    queue = sqs.get_queue_by_name(QueueName=APP_CONFIG.data_pip_sqs_consumer_queue_name)
    logger.info(f"Subscribing to queue {APP_CONFIG.data_pip_sqs_consumer_queue_name}")
    logger.info("SQS Consumer starting ...")

    # try:
    #     response = queue.send_message(
    #         MessageBody="this is a test"
    #     )
    # except Exception as error:
    #     logger.exception("Send message failed: %s", "this is a test")
    #     raise error

    while True:        
        messages = queue.receive_messages(
            MaxNumberOfMessages=1,
            WaitTimeSeconds=1
        )
        for message in messages:
            try:
                process_message_fn(message.body)
            except Exception as e:
                print(f"Exception while processing message: {repr(e)}")
                continue

            message.delete()

def producer(message=any):
    queue = sqs.get_queue_by_name(QueueName=APP_CONFIG.dash_sqs_consumer_queue_name)
    # logger.info(f"Subscribing to queue {APP_CONFIG.dash_sqs_consumer_queue_name}")
    logger.info("SQS Producer starting ...")
    queue.send_message(
        # QueueUrl='string',
        MessageBody=json.dumps(message),
        # DelaySeconds=123,
        # MessageAttributes={
        #     'string': {
        #         'StringValue': 'string',
        #         'BinaryValue': b'bytes',
        #         'StringListValues': [
        #             'string',
        #         ],
        #         'BinaryListValues': [
        #             b'bytes',
        #         ],
        #         'DataType': 'string'
        #     }
        # },
        # MessageSystemAttributes={
        #     'string': {
        #         'StringValue': 'string',
        #         'BinaryValue': b'bytes',
        #         'StringListValues': [
        #             'string',
        #         ],
        #         'BinaryListValues': [
        #             b'bytes',
        #         ],
        #         'DataType': 'string'
        #     }
        # },
        # MessageDeduplicationId='string',
        # MessageGroupId='string'
    )
