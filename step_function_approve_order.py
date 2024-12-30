import json
import time
import traceback
from datetime import datetime
import boto3

dynamodb = boto3.client('dynamodb')


def update_order_details(order_detail):
    """
    Create entry in to DynamoDB table and generate order_id
    :param order_detail: received approved order
    :return: order_id and creation time
    """
    # A
    order_id = str(int(time.time()))
    now = datetime.now()
    creation_time = now.strftime("%H:%M:%S")
    item_str = {'order_id': {'S': order_id}, 'creation_time': {'S': creation_time}, 'order': {'S': str(order_detail)},
                'payment_status': {'S': 'not_paid'},
                'shipment_status': {'S': 'not_shipped'}}
    response = dynamodb.put_item(TableName='food_order', Item=item_str)
    return order_id, creation_time


def lambda_handler(event, context):
    """
    The lambda invocation receives the approved order and creates the input in dynamoDB
    :param event: Data received by the AWS Lambda service
    :param context:  Information about the invocation, function, and execution environment
    :return: order_id, creation_time, order and the updated status
    """

    order_detail = event[0]["body"]
    try:
        order_id, creation_time = update_order_details(order_detail)
    except Exception as db_ex:
        traceback.print_exception(type(db_ex), value=db_ex, tb=db_ex.__traceback__)
    
    return {'statusCode': 200,
            'body': {
                'order_id': order_id,
                'creation_time': creation_time,
                'order': event[0]["body"],
                'updated': True
            }
            }


