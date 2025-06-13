import boto3
import json
import os
from urllib.parse import unquote_plus

# Initialize AWS clients
s3 = boto3.client('s3')
textract = boto3.client('textract')
sns = boto3.client('sns')

def lambda_handler(event, context):
    """
    This function is triggered when a new file is uploaded to the source S3 bucket.
    It processes the image with Textract and saves the results to another S3 bucket.
    """
    try:
        # 1. Get the uploaded file information from the S3 event
        record = event['Records'][0]['s3']
        source_bucket = record['bucket']['name']
        file_key = unquote_plus(record['object']['key'])
        
        print(f"Processing file: {file_key} from bucket: {source_bucket}")

        # 2. Download the file from S3
        response = s3.get_object(Bucket=source_bucket, Key=file_key)
        image_bytes = response['Body'].read()

        # 3. Process the image with Textract
        print("Starting Textract processing...")
        textract_response = textract.detect_document_text(
            Document={'Bytes': image_bytes}
        )
        
        # 4. Extract the text from the response
        extracted_text = []
        for item in textract_response['Blocks']:
            if item['BlockType'] == 'LINE':
                extracted_text.append(item['Text'])
        
        # Combine all lines into a single string
        full_text = '\n'.join(extracted_text)
        
        # 5. Prepare the results as JSON
        results = {
            'original_file': file_key,
            'extracted_text': full_text,
            'textract_response': textract_response  # Full response if needed
        }
        results_json = json.dumps(results, indent=2)

        # 6. Save results to the destination bucket
        results_key = f"results/{file_key.split('/')[-1]}_results.json"
        s3.put_object(
            Bucket=os.environ['RESULTS_BUCKET'],
            Key=results_key,
            Body=results_json,
            ContentType='application/json'
        )
        print(f"Results saved to S3: {results_key}")

        # 7. Send SNS notification
        sns.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Message=f"Textract processing complete for {file_key}. Results saved to {results_key}",
            Subject="Textract Processing Complete"
        )
        print("Notification sent to SNS")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Processing complete',
                'results_key': results_key
            })
        }

    except Exception as e:
        print(f"Error processing file: {str(e)}")
        # Send failure notification
        sns.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Message=f"Textract processing failed for {file_key}. Error: {str(e)}",
            Subject="Textract Processing Failed"
        )
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }