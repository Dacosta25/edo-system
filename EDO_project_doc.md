# edo-system — Event-Driven Order Processing (AWS SAM)

A fully serverless, event-driven order processing system built using AWS SAM.  
Includes staging + production CI/CD pipelines, CloudFront invalidation, environment variables, and production-ready architecture.

---

## 🚀 Features

- Event-driven architecture (SNS → SQS → Lambda)
- API Gateway + Lambda order API
- DynamoDB order storage
- CloudFront + S3 frontend hosting
- Full CI/CD (staging + production)
- CloudFront cache invalidation on deploy
- Discord/Slack deployment notifications
- Environment-specific configuration
- Production-ready folder structure
- Architecture diagrams + documentation

---

## 🏗️ Architecture Overview

### High-Level Flow

1. Client → CloudFront → API Gateway  
2. API Lambda → DynamoDB  
3. API Lambda → SNS Topic  
4. SNS → SQS Queues  
5. SQS → Worker Lambdas  
6. Worker Lambdas → DynamoDB updates / external APIs

### Components

- **API Gateway** — public entry point  
- **Order API Lambda** — validates requests, writes to DynamoDB, publishes events  
- **SNS Topic** — fan-out event distribution  
- **SQS Queues** — buffer events for workers  
- **Worker Lambdas** — payment, fulfillment, notifications  
- **DynamoDB** — order storage  
- **CloudFront + S3** — frontend hosting  
- **IAM Roles** — least privilege  
- **GitHub Actions CI/CD** — automated deployment

---

## 📦 Folder Structure

edo-system/
├── src/
│   ├── order_api/
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── workers/
│   │   ├── payment_worker.py
│   │   ├── fulfillment_worker.py
│   │   └── notification_worker.py
│   └── common/
│       ├── models.py
│       └── utils.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── infrastructure/
│   ├── template.yaml
│   └── parameters/
│       ├── staging.json
│       └── prod.json
│
├── .github/
│   └── workflows/
│       ├── staging.yaml
│       ├── production.yaml
│
├── docs/
│   ├── architecture.md
│   ├── deployment.md
│   ├── diagrams.txt
│   └── folder-structure.md
│
├── README.md
└── requirements.txt


---

## ⚙️ Environment Variables

Defined in `template.yaml`:

```yaml
Parameters:
  StageParameter:
    Type: String
    Default: staging
    AllowedValues:
      - staging
      - prod

Resources:
  OrderApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/order_api/app.handler
      Runtime: python3.10
      Environment:
        Variables:
          ORDERS_TABLE_NAME: Orders
          SNS_TOPIC_ARN: !Ref OrderEventsTopic
          STAGE: !Ref StageParameter

Deployment Instructions

Local Deployment
pip install -r requirements.txt
sam validate
sam build
sam deploy --stack-name edo-system-staging --capabilities CAPABILITY_IAM --region eu-west-2

CI/CD Deployment
Staging

git push origin staging

Production
git push origin main

GitHub Actions will automatically:

Build

Test

Deploy

Invalidate CloudFront

Notify Discord/Slack

📊 CI/CD Status
Staging
https://github.com/Dacosta25/edo-system/actions/workflows/staging.yaml/badge.svg

Production
https://github.com/Dacosta25/edo-system/actions/workflows/production.yaml/badge.svg

Documentation
See /docs folder:

architecture.md

deployment.md

diagrams.txt

folder-structure.md

🧠 Interview Talking Points
Event-driven architecture using SNS + SQS

Serverless compute using Lambda

API Gateway integration

DynamoDB single-table design

CI/CD with GitHub Actions

Multi-environment deployment (staging + production)

CloudFront invalidation

Infrastructure-as-code using AWS SAM

Least-privilege IAM roles

Automated testing pipeline