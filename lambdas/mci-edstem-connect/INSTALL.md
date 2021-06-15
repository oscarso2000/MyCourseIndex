The main instructions are here to create or update a lambda function: [link](https://docs.aws.amazon.com/lambda/latest/dg/python-package-create.html#python-package-create-with-dependency)

However for some more specifics, we can do the following:

1. Navigate to the Lambda page within the AWS console, and click *Create function*
2. Create a function with a Python 3.x runtime and a new execution role. Provide this role with the *AWSLambdaBasicExecutionRole* policy (this just gives the function permission to write to CloudWatch logs).
3. Navigate to the CloudWatch page within the AWS console, and click on _Events_ > _Rules_.
4. Create a new rule, using a schedule. Add your Lambda function as the target. Make sure to set this interval to be the same as you have configured within the function code (current value is 1 minutes).
5. Configure the AWS CLI on your local machine if you have not already. Install the CLI ([Mac instructions](https://docs.aws.amazon.com/cli/latest/userguide/install-macos.html)) the run `aws configure`. You can generate an access key ID and secret access key in the AWS console from _Your Name_ > _My Security Credentials_ > _Access keys_.
6. Follow the instructions describe [here](https://docs.aws.amazon.com/lambda/latest/dg/python-package-create.html#python-package-create-with-dependency) to create an AWS Lambda Deployment Package with Additional Dependencies, and deploy from your local system.
7. Return to the AWS console, and change the _handler_ field of your Lambda function to be `mci_edstem_connector.update_handler`

The bot will then send a notification to the MCI Elastisearch cluster whenever a new post is added to Piazza / EdStem.
