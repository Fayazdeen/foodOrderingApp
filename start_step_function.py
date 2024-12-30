import json
import boto3


def lambda_handler(event, context):
    """
     The lambda invocation starts the statemachine execution with required input data
    :param event: Data received by the AWS Lambda service
    :param context:  Information about the invocation, function, and execution environment
    :return: status code and order approval
    """
    client = boto3.client('stepfunctions')
    response = client.start_execution(
        stateMachineArn='arn:aws:states:p-south-1:431419466567:stateMachine:MyStateMachine-x7sqh7dxo',
        input=json.dumps(event["Records"])
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return {
            'order': 'approved',
            'statusCode': 200
        }
    else:
        print("response", response)
        raise Exception 
