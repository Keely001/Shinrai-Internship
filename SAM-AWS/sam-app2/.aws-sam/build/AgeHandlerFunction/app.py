import json            # To parse request bodies
import os              # To read environment variables
import boto3           # AWS SDK for Python

# Initialize SNS client
sns = boto3.client('sns')

# Read the SNS topic ARN from environment variables
TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):

    # Parse the request body (from API Gateway)
    body = json.loads(event['body'])

    # Safely extract values from the JSON, using defaults if missing
    name = body.get('name', 'User')
    age = int(body.get('age', 0))
    gender = body.get('gender', 'Not specified')
    
    try:

        # Check if the user is an adult (18+)
        if age >= 18:
            # Custom welcome message
            subject = "🎉 Welcome to Our Service"
            message = (
                f"Hello {name},\n\n"
                f"Welcome aboard! We're excited to have a {gender.lower()} participant like you in our community.\n\n"
                "Enjoy your journey!"
            )
        else:
            # Polite rejection message for underage users
            subject = "👋 Thanks for Your Interest"
            message = (
                f"Hi {name},\n\n"
                "Thanks for reaching out! You must be at least 18 years old to access this service.\n\n"
                "You're welcome back when the time comes!"
            )

        # Send the message to the SNS topic
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject=subject,
            Message=message
        )

        # Return HTTP 200 success response
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Email sent"})
        }

    except Exception as e:
        # Send custom error message to same SNS topic
        error_message = f"🚨An Itsy bitsy error on the server side occured:\n\nName: {name}\nAge: {age}\nGender: {gender}\n\n\n"
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject='Server Error',
            Message=error_message
        )

        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

