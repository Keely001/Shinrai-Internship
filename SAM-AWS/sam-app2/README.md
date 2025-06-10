# 📧 Age-Based Email Notification System (AWS SAM)

A serverless application built with **AWS SAM**, **Lambda**, **API Gateway**, and **Amazon SNS**.  
It receives user data via HTTP POST, checks their age, and sends a custom email message based on eligibility.

---

## 🧩 Features

- 🟢 Serverless architecture with AWS Lambda (Python)
- 🌐 Triggered by HTTP POST using API Gateway
- 📤 Sends emails via Amazon SNS
- 🔐 Environment variables and IAM-based access
- ⚙️ Built and deployed using AWS SAM CLI

---

## 📁 Project Structure

```
.
├── template.yaml        # SAM template for resources
├── src/
│   └── app.py           # Lambda function code
```

---

## 🚀 Deployment

```bash
sam build
sam deploy --guided
```

> This will package and deploy your Lambda, API Gateway, and SNS topic to AWS.

---

## 🧪 Testing the API

### ✅ Test with a user who is 18 or older

 '{"name": "Alice", "age": 25, "gender": "Female"}'

### ❌ Test with a user under 18

  -d '{"name": "Bob", "age": 16, "gender": "Male"}'

## 📬 Subscribe to the SNS Topic

NB: Check your inbox and confirm the subscription to start receiving emails.

---

## 🛠️ Requirements

- Python 3.13
- AWS SAM CLI
- AWS CLI (configured)
- An AWS account
- An email address to receive notifications

