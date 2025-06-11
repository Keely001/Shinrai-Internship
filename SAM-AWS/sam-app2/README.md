# Age-Based Email Notification System (AWS SAM)

A serverless application built with **AWS SAM**, **Lambda**, **API Gateway**, and **Amazon SNS**.  
It receives user data via HTTP POST, checks their age, and sends a custom email message based on eligibility.

---

## Features

- Serverless architecture with AWS Lambda (Python)
- Triggered by HTTP POST using API Gateway
- Sends emails via Amazon SNS
- Environment variables and IAM-based access
- Built and deployed using AWS SAM CLI
- CloudWatch logging and alarms for error detection

## Deployment

```bash
sam build
sam deploy --guided
```

> This will package and deploy your Lambda, API Gateway, and SNS topic to AWS.

---

## Testing the API

### Test with a user who is 18 or older

 '{"name": "Alice", "age": 25, "gender": "Female"}'

### Test with a user under 18

  '{"name": "Bob", "age": 16, "gender": "Male"}'

### Test with a user under 18

{"age": "invalid"}  # malformed input


## Subscribe to the SNS Topic

After deployment, subscribe your email to:

- AgeBasedWelcomeTopic for user messages

- LambdaErrorAlarmTopic for alarm alerts

NB: Check your inbox and confirm the subscription to start receiving emails.

---

## Requirements

- Python 3.13
- AWS SAM CLI
- AWS CLI (configured)
- An AWS account
- An email address to receive notifications
- Docker (for local testing)
