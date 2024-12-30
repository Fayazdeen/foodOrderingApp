import traceback

import boto3
import random

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('food_order')


def update_payment_status(order_id, creation_time):
    """
    Update the payment detail in the DynamoDB table for respective order_id
    :param order_id: ID of the order
    :param creation_time: timestamp it is created
    :return: status of the DB update operation
    """
    response = table.update_item(
        Key={
            'order_id': order_id,
            'creation_time': creation_time
        },
        UpdateExpression="set payment_status = :r",
        ExpressionAttributeValues={
            ':r': 'done',
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def lambda_handler(event, context):
    """
    Receives the order and attempts the payment processing and updates the dynamoDB
    :param event: Data received by the AWS Lambda service
    :param context:  Information about the invocation, function, and execution environment
    :return: order_id, creation_time, payment status and the updated status
    """
    L = [True, False]
    Payment_result = random.choice(L)

    if Payment_result:
        order_detail = event["body"]
        try:
            update_payment_status(order_detail["order_id"], order_detail["creation_time"])
        except Exception as db_ex:
            traceback.print_exception(type(db_ex), value=db_ex, tb=db_ex.__traceback__)

        return {'statusCode': 200,
                'body': {
                    'order_id': order_detail["order_id"],
                    'creation_time': order_detail["creation_time"],
                    'payment_status': True,
                    'updated': True
                }
                }
    else:
        raise Exception


