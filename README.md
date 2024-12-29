# foodOrderingApp
This repository has the step by step guidance and driver codes for the online food ordering application using AWS cloud services like #APIGateway#SQS#Stepfunction#Lambda#DynamoDB#SNS
# Steps to be followed:

# 1, IAM roles:

# for ApiGateway to Access SQS:
  
    * Go to IAM service. Click on **"Create Role"**
    * Choose "AWS Service" under trusted entity type.
    * In this case, we require AWS ApiGateway to publish the message to SQS.
    * Hence, attach the policies accordingly. For example, "AmazonSQSFullAccess" can be attached and then give a suitable name like "ApiGatewayToSQS"

# for Lambda to Access Step Function:
  
    * Go to IAM service. Click on **"Create Role"**
    * Choose "AWS Service" under trusted entity type.
    * In this case, we require AWS ApiGateway to publish the message to SQS.
    * Hence, attach the policies accordingly. For example, "AWSStepFunctionsFullAccess" can be attached and then give a suitable name like "LambdaToStepFunction". 


# 2, AWS SQS - Queue creation:

* Goto "AWS SQS> Queues> Create queue"
* Select Standard Queue and with queue name as "foodOrder"
* Then click "Create"

# 3, AWS API Gateway - Create API:

* Goto "AWS API Gateway> APIs> Create API"
* Choose Rest API > Build > New API
* Give a suitable name and choose Regional Option and then click "Create API"
* Click on the create resource and then create the resource as "placeOrder"
* Click on the "Create Method"
* Enter the following detail

* Method type : Get
* Integration type: AWS Service
* AWS Region: Your region
* AWS service: SQS
* HTTP method: POST
* Action type: Use path override
* Path override: Copy the SQS Queue URL from Step 1 and paste here
* Execution role: Paste the "ApiGatewayToSQS" role that you created in the step 1
* Request body passthrough: When no template matches the request content-type header
* Mapping templates:
    application/json
    Template body:
    Action=SendMessage&MessageBody=$util.urlEncode($input.body)
  
# 4, AWS Lambda - StartStepFunction:

* Create a **lambda function**
* Give a suitable name under "Function Name"
* Choose the suitable Runtime: "Python 3.10" and Architecture: "x86_64"
* Under the "Change default execution role", choose use existing role and give the "LambdaToStepFunction" role that we have created in step 1.
* In the code section, paste the content of "StartStepFunction.py".
* Also Configure the test event. Click on "Configure test event". Choose "Create test event". Give a suitable name and choose "Private". Under the Event JSON, paste the following test event: {
  "idly": "1",
  "poori": "2"
}
* Deploy the lambda function

# 4, AWS Lambda - stepFunction-approve-order:

* Create a **lambda function**
* Give a suitable name under "Function Name"
* Choose the suitable Runtime: "Python 3.10" and Architecture: "x86_64"
* Under the "Change default execution role", choose use existing role and give the "LambdaToStepFunction" role that we have created in step 1.
* In the code section, paste the content of "StartStepFunction.py".
* Also Configure the test event. Click on "Configure test event". Choose "Create test event". Give a suitable name and choose "Private". Under the Event JSON, paste the following test event: {
  "idly": "1",
  "poori": "2"
}
* Deploy the lambda function

# 4, AWS Lambda - stepFunction-ship-order:

* Create a **lambda function**
* Give a suitable name under "Function Name"
* Choose the suitable Runtime: "Python 3.10" and Architecture: "x86_64"
* Under the "Change default execution role", choose use existing role and give the "LambdaToStepFunction" role that we have created in step 1.
* In the code section, paste the content of "StartStepFunction.py".
* Also Configure the test event. Click on "Configure test event". Choose "Create test event". Give a suitable name and choose "Private". Under the Event JSON, paste the following test event: {
  "idly": "1",
  "poori": "2"
}
* Deploy the lambda function

# 5, Configure Lambda trigger for SQS Queue:

* Goto the "SQS>Queues>foodOrder>Lambda triggers"
* Click on the "Configure lambda function trigger"
* Specify the lambda arn of "StartStepFunction" lambda from step 4

# 6, Configure Lambda trigger for SQS Queue:

