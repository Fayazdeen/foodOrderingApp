# foodOrderingApp
This repository has the step by step guidance and driver codes for the online food ordering application using AWS cloud services like #APIGateway#SQS#Stepfunction#Lambda#DynamoDB#SNS
# Steps to be followed:

# 1, IAM roles:

# for ApiGateway to Access SQS:
  
    * Go to IAM service. Click on **"Create Role"**
    * Choose "AWS Service" under trusted entity type.
    * In this case, we require AWS ApiGateway to publish the message to SQS.
    * Hence, attach the policies accordingly. For example, "AmazonSQSFullAccess" can be attached and then give a suitable name like "ApiGatewayToSQS"

# for Lambda to Start StateMachine in Step Function:
  
    * Go to IAM service. Click on **"Create Role"**
    * Choose "AWS Service" under trusted entity type.
    * In this case, we require AWS ApiGateway to publish the message to SQS.
    * Hence, attach the policies accordingly. For example, "AWSStepFunctionsFullAccess" can be attached and then give a suitable name like "LambdaToStepFunction". 

# for Lambda to get,put and update item in DynamoDB table:
  
    * Go to IAM service. Click on **"Create Role"**
    * Choose "AWS Service" under trusted entity type.
    * In this case, we require AWS ApiGateway to publish the message to SQS.
    * Hence, attach the policies accordingly. For example, "AmazonDynamoDBFullAccess" can be attached and then give a suitable name like "LambdaToDynamoDB". 


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
* Deploy the api with stage name as "test"
  
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

# 5, AWS Lambda - stepFunction-approve-order:

* Create a **lambda function**
* Give a suitable name under "Function Name"
* Choose the suitable Runtime: "Python 3.10" and Architecture: "x86_64"
* Under the "Change default execution role", choose use existing role and give the "LambdaToDynamoDB" role that we have created in step 1.
* In the code section, paste the content of "sf_approve_order.py".
* Deploy the lambda function

# 6, AWS Lambda - stepFunction-process-payment:

* Create a **lambda function**
* Give a suitable name under "Function Name"
* Choose the suitable Runtime: "Python 3.10" and Architecture: "x86_64"
* Under the "Change default execution role", choose use existing role and give the "LambdaToDynamoDB" role that we have created in step 1.
* In the code section, paste the content of "sf_process_payment.py".
* Deploy the lambda function

# 7, AWS Lambda - stepFunction-ship-order:

* Create a **lambda function**
* Give a suitable name under "Function Name"
* Choose the suitable Runtime: "Python 3.10" and Architecture: "x86_64"
* Under the "Change default execution role", choose use existing role and give the "LambdaToDynamoDB" role that we have created in step 1.
* In the code section, paste the content of "sf_ship_order.py".
* Deploy the lambda function

# 8, Configure AWS SNS Topic:

* Go to AWS SNS Service
* Choose **"Topics > Choose Topic"**
* Choose "Standard" Type
* Provide "Name" and "Display Name"
* Once the Topic is created, click on "Subscription". Choose "Email" under protocol and enter your "Email address" in the  Endpoint field . Click on "Create Subscription". 
* You would have received the Notification from AWS SNS Service. Click on the link to subscribe for the topic.

# 9, Create AWS DynamoDB table:

* Go to AWS DynamoDB service.
* Choose **"Tables > Create Table"**
* Give the table name as "food_order"
* Give "order_id" as Partition key and "creation_time" as Sort Key. Then create the table with default setting.

# 10, Create Statemachine in Step Function:

* In order to create the state machine for the step function, use the step_function_state_machine.json file.
* Update the 4 lambda function arns from step 4,5,6 and 7 above.
* Go to "AWS Step functions > State Machines > Create State Machine"
* Choose Blank and click on "Select"
* Then toggle to the **{}code** option
* Paste the updated json content of the step_function_state_machine.json
* Then click create
* The required StateMachine tasks will be configured.
* Copy the above statemachine arn and update the StartStepFunction.py lambda code and Redeploy the StartStepFunction lambda.

# Demo: 

* Now from the postman, trigger the API that you have created in step 3. Pass the following content as Body(raw):
   {
     "messageType":"approval",
     "order": [
        {
           "idly":"3"
        },
        {
           "poori":"2"
        }
     ]
  }
* Eventually, after the suitable processing at the stepfunction, the message will be published to the subscribed email id.

  

