# System Architecture — edo-system

## Overview
The edo-system is an event-driven order processing platform built using AWS Serverless Application Model (SAM). It processes customer orders, triggers downstream workflows, and updates order state using a fully serverless architecture.

## Components

### 1. API Gateway
Acts as the public entry point for all client requests:
- Create order
- Get order status
- Update order

### 2. Lambda Functions
#### Order API Lambda
- Validates incoming requests
- Writes order data to DynamoDB
- Publishes events to SNS

#### Worker Lambdas
- **Payment Worker** — processes payments
- **Fulfillment Worker** — handles order fulfillment
- **Notification Worker** — sends email/SMS updates

### 3. DynamoDB
- `Orders` table stores order metadata and state
- Optional `OrderEvents` table stores audit logs

### 4. SNS Topic — OrderEvents
Fan-out event distribution to multiple consumers.

### 5. SQS Queues
SNS → SQS → Worker Lambdas
- PaymentQueue
- FulfillmentQueue
- NotificationQueue

### 6. S3 + CloudFront
- S3 hosts static frontend
- CloudFront caches and serves global content
- CI/CD triggers invalidation on deploy

### 7. IAM Roles
Least-privilege roles for:
- API Lambda
- Worker Lambdas
- Deployment pipeline (CloudFormation, Lambda, DynamoDB, CloudFront)

## High-Level Flow
1. Client → CloudFront → API Gateway  
2. API Lambda → DynamoDB  
3. API Lambda → SNS  
4. SNS → SQS  
5. SQS → Worker Lambdas  
6. Worker Lambdas → DynamoDB updates / external APIs