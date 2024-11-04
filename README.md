**Project Overview**

This repository contains the core code for a serverless application that mirrors API Gateway logs to an EC2 instance, where they are processed and stored in a PostgreSQL database.

**Use Case**

    API Gateway Event Trigger:
        An HTTP API is deployed on AWS API Gateway.
        API Gateway invokes the Lambda function whenever an API request is received.

    Lambda Function:
        The Lambda function retrieves the API Gateway log events from CloudWatch Logs.
        The log data is processed (e.g., parsed, filtered) as needed.
        The processed data is sent to the EC2 instance using an HTTP POST request.

    EC2 Instance:
        The EC2 instance hosts a web server that listens for incoming HTTP requests.
        Upon receiving a request from the Lambda function, the server processes the log data further.
        The processed data is stored in a PostgreSQL database for analysis and auditing.

**Deployment and Configuration**

To deploy and configure this application, you'll need to:

    Create AWS Resources:
        Set up an API Gateway API with the desired endpoints.
        Create an IAM role for the Lambda function with necessary permissions to access CloudWatch Logs and make HTTP requests.
        Deploy the Lambda function and configure the CloudWatch trigger.
        Launch an EC2 instance and configure its security group to allow incoming HTTP requests.
        Set up a PostgreSQL database on the EC2 instance or a managed database service.

    Configure the Application:
        Update the Lambda function code to point to the correct CloudWatch log group and the EC2 instance's endpoint.
        Configure the EC2 instance's web server to process incoming requests and store data in the database.
