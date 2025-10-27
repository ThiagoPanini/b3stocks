<div align="center">
    <br><img src="https://github.com/ThiagoPanini/b3stocks/blob/main/docs/imgs/logo-b3stocks.png?raw=true" width=200 alt="b3stocks-logo">
</div>

<div align="center">

  <a href="https://www.terraform.io/">
    <img src="https://custom-icon-badges.demolab.com/badge/AWS-%23FF9900.svg?logo=aws&logoColor=white&style=for-the-badge&color=555555">
  </a>

  <a href="https://www.terraform.io/">
    <img src="https://img.shields.io/badge/python-grey?style=for-the-badge&logo=python&logoColor=FFFFFF">
  </a>

  <a href="https://www.terraform.io/">
    <img src="https://img.shields.io/badge/terraform-grey?style=for-the-badge&logo=terraform&logoColor=FFFFFF">
  </a>

  <a href="https://www.hashicorp.com/">
    <img src="https://img.shields.io/badge/hashicorp-grey?style=for-the-badge&logo=hashicorp&logoColor=FFFFFF">
  </a>

  <a href="https://github.com/">
    <img src="https://img.shields.io/badge/github-grey?style=for-the-badge&logo=github&logoColor=FFFFFF">
  </a>

  <a href="https://github.com/copilot">
    <img src="https://img.shields.io/badge/copilot-grey?style=for-the-badge&logo=githubcopilot&logoColor=FFFFFF">
  </a>
</div>

<br>

# 💰 b3stocks: Serverless Data Pipeline for Brazilian Stock Market

> **A serverless, event-driven data platform for collecting, processing, and analyzing Brazilian stock market data (B3) using AWS services**

<br>

---

## 📋 Table of Contents

- [💰 b3stocks: Serverless Data Pipeline for Brazilian Stock Market](#-b3stocks-serverless-data-pipeline-for-brazilian-stock-market)
  - [📋 Table of Contents](#-table-of-contents)
  - [🎯 Overview](#-overview)
    - [Who Is It For?](#who-is-it-for)
  - [✨ Main Features](#-main-features)
    - [🔄 Automated Data Collection](#-automated-data-collection)
    - [📊 Multi-Layer Data Architecture](#-multi-layer-data-architecture)
    - [🚀 Event-Driven Processing](#-event-driven-processing)
    - [📧 Intelligent Notifications](#-intelligent-notifications)
    - [🏗️ Clean Architecture Implementation](#️-clean-architecture-implementation)
  - [🏛️ Architecture and Code Structure](#️-architecture-and-code-structure)
    - [High-Level Architecture](#high-level-architecture)
    - [Data Flow](#data-flow)
    - [Clean Architecture Principles](#clean-architecture-principles)
      - [Layered Structure (Inside-Out)](#layered-structure-inside-out)
      - [Benefits of This Architecture](#benefits-of-this-architecture)
  - [🛠️ Technologies Used](#️-technologies-used)
    - [Core Technologies](#core-technologies)
    - [Python Libraries](#python-libraries)
    - [AWS Services](#aws-services)
    - [Why These Technologies?](#why-these-technologies)
  - [🚀 Installation and Execution](#-installation-and-execution)
    - [Prerequisites](#prerequisites)
    - [Local Development Setup](#local-development-setup)
    - [Infrastructure Deployment](#infrastructure-deployment)
    - [Running the Pipeline](#running-the-pipeline)
    - [Local Testing (Optional)](#local-testing-optional)
  - [🧪 Testing](#-testing)
    - [Test Structure](#test-structure)
    - [Running Unit Tests](#running-unit-tests)
    - [Integration Testing](#integration-testing)
    - [Testing Batch Completion Emails](#testing-batch-completion-emails)
  - [🏗️ Deployment \& Infrastructure](#️-deployment--infrastructure)
    - [AWS Services Overview](#aws-services-overview)
    - [Infrastructure Components](#infrastructure-components)
      - [1. **DynamoDB Tables**](#1-dynamodb-tables)
      - [2. **Lambda Functions**](#2-lambda-functions)
      - [3. **S3 Buckets**](#3-s3-buckets)
      - [4. **AWS Glue Data Catalog**](#4-aws-glue-data-catalog)
      - [5. **SNS Topics**](#5-sns-topics)
      - [6. **SQS Queues**](#6-sqs-queues)
    - [Deployment Process](#deployment-process)
    - [Cost Estimation](#cost-estimation)
  - [🤝 Contributing](#-contributing)
    - [How to Contribute](#how-to-contribute)
    - [Coding Conventions](#coding-conventions)
    - [Branching Strategy](#branching-strategy)
    - [Reporting Issues](#reporting-issues)
    - [⭐ Star this repository if you find it useful!](#-star-this-repository-if-you-find-it-useful)

---

## 🎯 Overview

**b3stocks** is a fully serverless, event-driven data platform built on AWS that automatically collects, processes, and analyzes stock market data from the Brazilian stock exchange (B3). The system scrapes data from publicly available sources like Fundamentus, stores it in a multi-layered data architecture (CDC and System of Record), and provides real-time processing capabilities through DynamoDB Streams.

### Who Is It For?

- **Individual investors** who want to track Brazilian stocks and portfolios automatically
- **Data engineers** looking for a reference implementation of a serverless data pipeline
- **Python developers** interested in Clean Architecture applied to AWS Lambda functions
- **Infrastructure engineers** seeking Terraform-based AWS infrastructure patterns

---

## ✨ Main Features

### 🔄 Automated Data Collection

- **Active Stocks Scraping**: Daily scheduled scraping of all active B3 stocks from Fundamentus website
- **End-of-Day Metrics**: Automatic collection of comprehensive stock metrics including valuation ratios, financial indicators, and price data

### 📊 Multi-Layer Data Architecture

- **Change Data Capture (CDC)**: Real-time streaming of data changes from DynamoDB to S3 as JSON records
- **System of Record (SoR)**: Processed, cleaned data stored in Parquet format optimized for analytics queries
- **AWS Glue Data Catalog**: Automatic schema discovery and metadata management for both CDC and SoR datasets

### 🚀 Event-Driven Processing

- **DynamoDB Streams**: Real-time CDC processing for all database changes
- **SNS/SQS Integration**: Decoupled message-driven architecture for scalable processing
- **Batch Process Tracking**: Monitors long-running processes and sends completion emails with detailed reports

### 📧 Intelligent Notifications

- **Batch Completion Emails**: Automated HTML emails via AWS SES when batch processes complete
- **Email Templates**: S3-stored HTML templates with dynamic placeholder replacement
- **Process Status Tracking**: Real-time tracking of batch processes with completion percentage

### 🏗️ Clean Architecture Implementation

- **Domain-Driven Design**: Business logic separated from infrastructure concerns
- **Interface Adapters**: Abstraction layers for all external services (DynamoDB, S3, SNS, SES)
- **Use Case Layer**: Self-contained business logic that can be tested independently
- **Presentation Layer**: AWS Lambda handlers that orchestrate use cases

---

## 🏛️ Architecture and Code Structure

### High-Level Architecture

The **b3stocks** platform follows a serverless, event-driven architecture built entirely on AWS managed services:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Event Triggers (EventBridge)                    │
│                          Daily @ 21:00 UTC                          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
         ┌───────────────────────────────────────────────┐
         │  Lambda: delete-already-processed-partitions  │
         │  (Prepares SoR tables for new data)           │
         └───────────────┬───────────────────────────────┘
                         │ invokes
                         ▼
         ┌───────────────────────────────────────────────┐
         │  Lambda: get-active-stocks                    │
         │  (Scrapes B3 stocks from Fundamentus)         │
         └───────────────┬───────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────────────────────┐
         │  DynamoDB: tbl_b3stocks_active_stocks         │
         │  (Stores active stock data)                   │
         └───────────────┬───────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    [DynamoDB      [SNS Topic]     [Lambda Stream]
     Streams]                       (CDC Processing)
         │               │               │
         │               ▼               ▼
         │          ┌─────────┐     ┌──────────┐
         │          │   SQS   │     │ S3 (CDC) │
         │          │  Queue  │     │ S3 (SoR) │
         │          └────┬────┘     └──────────┘
         │               │               │
         │               ▼               ▼
         │     ┌──────────────────┐  [Glue Catalog]
         │     │ Lambda: get-eod- │
         │     │ stock-metrics    │
         │     └────────┬─────────┘
         │              │
         │              ▼
         │     ┌──────────────────────────────┐
         │     │ DynamoDB: eod_stock_metrics  │
         │     └──────────────────────────────┘
         │
         ▼
    [Batch Process Tracking]
         │
         ▼
    [Email Notifications via SES]
```

### Data Flow

The data pipeline operates in the following sequence:

1. **Scheduled Trigger** (EventBridge @ 21:00 UTC daily)
   - Initiates the `delete-already-processed-partitions` Lambda
   - Cleans up SoR Glue tables by dropping partitions that will be reprocessed

2. **Active Stocks Collection**
   - Lambda scrapes Fundamentus website for all active B3 stocks
   - Parses HTML content to extract stock codes and company names
   - Batch inserts records into DynamoDB (`tbl_b3stocks_active_stocks`)
   - Publishes messages to SNS topic for downstream processing

3. **DynamoDB Streams Processing (CDC)**
   - Every insert/update/delete on DynamoDB tables triggers stream events
   - Lambda functions (`stream-*`) capture these events
   - Raw CDC data stored in S3 as JSON (partitioned by `event_date`)
   - Processed SoR data stored in S3 as Parquet (partitioned by `execution_date`)
   - AWS Glue Data Catalog automatically synced for schema discovery

4. **SNS to SQS Fan-Out**
   - SNS topic publishes stock codes to subscribed SQS queue
   - SQS queue buffers messages for controlled Lambda invocation
   - Lambda polls SQS in batches (max 100 messages, 10s batching window)

5. **End-of-Day Metrics Collection**
   - For each stock code from SQS, Lambda scrapes detailed metrics from Fundamentus
   - Parses financial indicators (P/E ratio, ROE, dividend yield, etc.)
   - Stores metrics in DynamoDB (`tbl_b3stocks_fundamentus_eod_stock_metrics`)

6. **Batch Process Tracking**
   - Each Lambda updates batch process control table with progress
   - When all items processed, batch status changes to "COMPLETED"
   - DynamoDB Stream triggers `check-batch-processes-completion` Lambda
   - Completion event published to SNS topic

7. **Email Notifications**
   - SNS message triggers `send-batch-completion-emails` Lambda
   - Fetches HTML template from S3
   - Replaces placeholders with actual process data
   - Sends formatted email via AWS SES

### Clean Architecture Principles

The codebase strictly follows **Clean Architecture** and **SOLID principles**:

#### Layered Structure (Inside-Out)

1. **Domain Layer** (`domain/`)
   - **Entities**: Pure business objects (`Stock`, `BatchProcess`, `FundamentusStockMetrics`)
   - **Value Objects**: Immutable types (`StockType`, `DateFormat`, `Timezone`, `BatchProcessName`)
   - **Interfaces**: Abstract contracts for infrastructure (`IHTTPClientAdapter`, `IDatabaseRepository`, `ITopicAdapter`)
   - **DTOs**: Data Transfer Objects for cross-layer communication (`InputDTO`, `OutputDTO`)

2. **Use Case Layer** (`use_case/`)
   - Self-contained business logic orchestration
   - Depends only on domain interfaces (Dependency Inversion Principle)
   - Examples: `GetActiveStocksUseCase`, `StoreDynamoDBStreamsDataUseCase`

3. **Infrastructure Layer** (`infra/`)
   - **Adapters**: Concrete implementations of domain interfaces
     - `RequestsHTTPClientAdapter`: HTTP requests via `requests` library
     - `FundamentusHTMLParserAdapter`: HTML parsing via `BeautifulSoup`
     - `DynamoDBDatabaseRepository`: Data persistence via `pynamodb`
     - `SNSTopicAdapter`: Message publishing via `boto3`
     - `AWSWranglerCDCDataCatalogSyncAdapter`: S3/Glue sync via `awswrangler`
   - **Mappers**: Transform external data formats to domain entities

4. **Presentation Layer** (`presentation/`)
   - AWS Lambda handler functions
   - Initializes adapters, repositories, and use cases
   - Maps Lambda events to domain DTOs
   - Returns HTTP-formatted responses

#### Benefits of This Architecture

- **Testability**: Use cases can be unit tested with mocked interfaces
- **Independence**: Business logic doesn't depend on AWS, databases, or frameworks
- **Flexibility**: Easy to swap implementations (e.g., replace DynamoDB with PostgreSQL)
- **Maintainability**: Clear separation of concerns makes code easy to understand and modify
- **Reusability**: Shared domain logic and utilities across multiple features

---

## 🛠️ Technologies Used

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.12 | Primary programming language for all Lambda functions |
| **Terraform** | ≥ 1.9 | Infrastructure as Code for AWS resource provisioning |
| **AWS Lambda** | - | Serverless compute for all data processing logic |
| **AWS DynamoDB** | - | NoSQL database for stock data, portfolios, and batch tracking |
| **AWS S3** | - | Object storage for CDC/SoR data, templates, and artifacts |
| **AWS Glue** | - | Data Catalog for schema management and metadata |

### Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| **pynamodb** | 6.1.0 | DynamoDB ORM for table operations |
| **boto3** | 1.36.23 | AWS SDK for Python (S3, SNS, SES, Lambda) |
| **PyYAML** | 6.0.2 | Parse YAML investment portfolio files |
| **awswrangler** | 3.13.0 | High-level AWS data operations (S3, Glue, Athena) |
| **requests** | 2.32.3 | HTTP client for web scraping |
| **beautifulsoup4** | 4.13.3 | HTML parsing for Fundamentus data extraction |
| **lxml** | 5.3.1 | Fast XML/HTML parser backend |

### AWS Services

- **AWS EventBridge**: Scheduled cron triggers for daily data collection
- **AWS SNS (Simple Notification Service)**: Pub/sub messaging for event distribution
- **AWS SQS (Simple Queue Service)**: Message buffering and controlled Lambda invocation
- **AWS SES (Simple Email Service)**: Transactional email delivery for batch notifications
- **AWS CloudWatch**: Logging, monitoring, and observability
- **AWS IAM**: Fine-grained access control and Lambda execution roles
- **AWS KMS**: Encryption key management for SNS topics

### Why These Technologies?

- **Serverless Architecture**: No servers to manage, automatic scaling, pay-per-use pricing
- **Event-Driven Design**: Decoupled components, easier to maintain and extend
- **Terraform**: Version-controlled infrastructure, reproducible deployments, modularity
- **Python 3.12**: Modern language features, excellent AWS SDK support, strong data processing ecosystem
- **DynamoDB**: Single-digit millisecond latency, built-in CDC via Streams, scales automatically
- **S3 + Glue + Athena**: Cost-effective data lake architecture, SQL queries over Parquet files

---

## 🚀 Installation and Execution

### Prerequisites

Before you begin, ensure you have the following tools installed and configured:

- **AWS Account**: Active AWS account with administrative access
- **AWS CLI**: Configured with credentials (`aws configure`)
  ```bash
  aws --version  # Should be ≥ 2.0
  ```
- **Terraform**: Version ≥ 1.9
  ```bash
  terraform --version
  ```
- **Python**: Version 3.12
  ```bash
  python3 --version
  ```
- **Git**: For cloning the repository
  ```bash
  git --version
  ```

### Local Development Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/ThiagoPanini/b3stocks.git
   cd b3stocks
   ```

2. **Create Python Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python Dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set Environment Variables** (for local testing)

   Create a `.env` file in the project root:

   ```bash
   # DynamoDB Tables
   export DYNAMODB_ACTIVE_STOCKS_TABLE_NAME="tbl_b3stocks_active_stocks"
   export DYNAMODB_INVESTMENT_PORTFOLIO_TABLE_NAME="tbl_b3stocks_investment_portfolio"
   export DYNAMODB_FUNDAMENTUS_EOD_STOCK_METRICS_TABLE_NAME="tbl_b3stocks_fundamentus_eod_stock_metrics"
   export DYNAMODB_BATCH_PROCESS_CONTROL_TABLE_NAME="tbl_b3stocks_batch_process_control"
   
   # SNS Topics
   export SNS_ACTIVE_STOCKS_TOPIC_NAME="b3stocks-active-stocks"
   export SNS_BATCH_PROCESSES_COMPLETION_TOPIC_NAME="b3stocks-batch-processes-completion"
   
   # S3 Buckets
   export S3_ARTIFACTS_BUCKET_NAME_PREFIX="b3stocks-artifacts"
   export S3_ANALYTICS_CDC_BUCKET_NAME_PREFIX="b3stocks-analytics-cdc"
   export S3_ANALYTICS_SOR_BUCKET_NAME_PREFIX="b3stocks-analytics-sor"
   
   # SES Configuration
   export SES_SENDER_EMAIL="your-email@example.com"
   
   # Glue Data Catalog
   export DATA_CATALOG_CDC_DATABASE_NAME="db_b3stocks_analytics_cdc"
   export DATA_CATALOG_SOR_DATABASE_NAME="db_b3stocks_analytics_sor"
   ```

   Load environment variables:
   ```bash
   source .env
   ```

5. **Configure AWS Credentials**

   Ensure your AWS credentials are configured:
   ```bash
   aws configure
   # Enter your AWS Access Key ID, Secret Access Key, Region, and Output format
   ```

### Infrastructure Deployment

1. **Navigate to Infrastructure Directory**

   ```bash
   cd infra
   ```

2. **Initialize Terraform**

   ```bash
   terraform init
   ```

   This downloads required Terraform providers and modules.

3. **Customize Variables** (Optional)

   Edit `variables.tf` or create a `terraform.tfvars` file:

   ```hcl
   # terraform.tfvars
   s3_artifacts_bucket_name_prefix = "my-custom-artifacts"
   ses_verified_emails = ["your-email@example.com"]
   
   tags = {
     Project     = "b3stocks"
     Environment = "production"
     ManagedBy   = "Terraform"
   }
   ```

4. **Review Terraform Plan**

   ```bash
   terraform plan
   ```

   Review all resources that will be created.

5. **Apply Infrastructure**

   ```bash
   terraform apply
   ```

   Type `yes` when prompted to confirm resource creation.

   **Expected Resources Created:**
   - 4 DynamoDB tables
   - 3 S3 buckets
   - 10+ Lambda functions
   - 2 Glue databases
   - Multiple Glue tables
   - SNS topics and SQS queues
   - IAM roles and policies
   - EventBridge rules
   - SES email identities

6. **Verify Deployment**

   ```bash
   # List Lambda functions
   aws lambda list-functions --query 'Functions[?contains(FunctionName, `b3stocks`)].FunctionName'
   
   # List DynamoDB tables
   aws dynamodb list-tables --query 'TableNames[?contains(@, `b3stocks`)]'
   
   # List S3 buckets
   aws s3 ls | grep b3stocks
   ```

7. **Verify SES Email Identity**

   After deployment, you'll receive a verification email from AWS SES. Click the link to verify your email address for sending notifications.

### Running the Pipeline

Once deployed, the pipeline runs automatically via EventBridge schedules:

- **Daily @ 21:00 UTC**: All Lambda functions trigger in sequence

To manually invoke a Lambda function:

```bash
# Invoke get-active-stocks Lambda
aws lambda invoke \
  --function-name b3stocks-get-active-stocks \
  --payload '{}' \
  response.json

cat response.json
```

### Local Testing (Optional)

To test Lambda functions locally without deploying:

```bash
cd app

# Example: Test get_active_stocks use case
python -c "
from app.src.features.get_active_stocks.presentation.get_active_stocks_presentation import handler
result = handler({}, None)
print(result)
"
```

---

## 🧪 Testing

### Test Structure

The project includes test infrastructure in the `app/tests/` directory:

```
app/tests/
├── local/          # Local development tests
├── mocks/          # Mock data and fixtures
└── notebooks/      # Jupyter notebooks for exploratory testing
```

### Running Unit Tests

Currently, the project is focused on integration testing via deployed Lambda functions. To run local tests:

```bash
cd app
python -m pytest tests/
```

*(Note: Based on the project structure analysis, formal unit tests are still in development. The current approach relies on AWS Lambda execution logs and CloudWatch monitoring.)*

### Integration Testing

Test deployed Lambda functions:

1. **Test via AWS Console**:
   - Navigate to AWS Lambda Console
   - Select a function (e.g., `b3stocks-get-active-stocks`)
   - Click "Test" tab
   - Create a test event with `{}`
   - Click "Test" and review execution results

2. **Test via AWS CLI**:

   ```bash
   aws lambda invoke \
     --function-name b3stocks-get-active-stocks \
     --log-type Tail \
     --query 'LogResult' \
     --output text \
     response.json | base64 --decode
   ```

3. **Monitor CloudWatch Logs**:

   ```bash
   aws logs tail /aws/lambda/b3stocks-get-active-stocks --follow
   ```

### Testing Batch Completion Emails

To test email notifications:

1. Ensure SES email is verified
2. Manually update a batch process in DynamoDB to "COMPLETED" status
3. DynamoDB Stream will trigger the notification flow
4. Check your email inbox for the batch completion report

---

## 🏗️ Deployment & Infrastructure

### AWS Services Overview

The **b3stocks** platform leverages the following AWS services:

| Service | Purpose | Key Features Used |
|---------|---------|-------------------|
| **Lambda** | Serverless compute | Python 3.12 runtime, EventBridge triggers, DynamoDB Streams, SQS polling |
| **DynamoDB** | NoSQL database | Streams (CDC), Batch operations, Global secondary indexes |
| **S3** | Object storage | Bucket policies, Lifecycle policies, Event notifications |
| **Glue** | Data Catalog | Databases, Tables, Partitions, Schema evolution |
| **EventBridge** | Scheduling | Cron expressions, Rule targets |
| **SNS** | Pub/Sub messaging | Topic subscriptions, Message filtering, KMS encryption |
| **SQS** | Message queuing | FIFO/Standard queues, Dead letter queues, Visibility timeout |
| **SES** | Email service | Email templates, HTML emails, Verified identities |
| **IAM** | Access control | Least privilege roles, Trust policies, Service-linked roles |
| **CloudWatch** | Observability | Logs, Metrics, Alarms, Dashboards |

### Infrastructure Components

#### 1. **DynamoDB Tables**

| Table Name | Purpose | Partition Key | Sort Key | Streams Enabled |
|------------|---------|---------------|----------|-----------------|
| `tbl_b3stocks_active_stocks` | Stores active B3 stocks | `code` (S) | - | ✅ NEW_AND_OLD_IMAGES |
| `tbl_b3stocks_investment_portfolio` | User portfolios | `owner_mail` (S) | - | ✅ NEW_AND_OLD_IMAGES |
| `tbl_b3stocks_fundamentus_eod_stock_metrics` | Daily stock metrics | `nome_papel` (S) | `execution_date` (S) | ✅ NEW_AND_OLD_IMAGES |
| `tbl_b3stocks_batch_process_control` | Batch tracking | `process_name` (S) | - | ✅ NEW_AND_OLD_IMAGES |

#### 2. **Lambda Functions**

**Core Processing Functions:**
- `b3stocks-delete-already-processed-partitions`: Drops Glue table partitions before reprocessing
- `b3stocks-get-active-stocks`: Scrapes active stocks from Fundamentus
- `b3stocks-get-fundamentus-eod-stock-metrics`: Collects detailed stock metrics
- `b3stocks-get-investment-portfolios`: Processes user portfolios from S3

**Stream Processing Functions:**
- `b3stocks-stream-active-stocks`: Processes CDC events from active stocks table
- `b3stocks-stream-fundamentus-eod-stock-metrics`: Processes CDC events from metrics table
- `b3stocks-stream-batch-process-control`: Monitors batch completion

**Notification Functions:**
- `b3stocks-check-batch-processes-completion`: Detects completed batches
- `b3stocks-send-batch-completion-emails`: Sends HTML email notifications

#### 3. **S3 Buckets**

| Bucket Name Pattern | Purpose | Contents |
|---------------------|---------|----------|
| `b3stocks-artifacts-<account>-<region>` | Artifacts storage | Portfolio YAML files, Email HTML templates |
| `b3stocks-analytics-cdc-<account>-<region>` | CDC data lake | JSON records partitioned by `event_date` |
| `b3stocks-analytics-sor-<account>-<region>` | SoR data lake | Parquet files partitioned by `execution_date` |

#### 4. **AWS Glue Data Catalog**

**Databases:**
- `db_b3stocks_analytics_cdc`: CDC datasets (JSON format)
- `db_b3stocks_analytics_sor`: System of Record datasets (Parquet format)

**Tables** (auto-synced via awswrangler):
- CDC tables: `active_stocks_cdc`, `fundamentus_eod_stock_metrics_cdc`
- SoR tables: `active_stocks_sor`, `fundamentus_eod_stock_metrics_sor`

#### 5. **SNS Topics**

- `b3stocks-active-stocks`: Publishes stock codes for downstream processing
- `b3stocks-batch-processes-completion`: Publishes batch completion events

#### 6. **SQS Queues**

- `b3stocks-fundamentus-eod-stock-metrics`: Buffers stock codes from SNS
- `b3stocks-fundamentus-eod-stock-metrics-dlq`: Dead letter queue for failed messages

### Deployment Process

The deployment follows this workflow:

1. **Terraform Init**: Downloads providers and modules
2. **Terraform Plan**: Generates execution plan
3. **Terraform Apply**: Creates/updates AWS resources
   - IAM roles and policies
   - S3 buckets
   - DynamoDB tables
   - Lambda functions (zips source code and uploads)
   - EventBridge rules
   - SNS/SQS resources
   - Glue databases and tables
   - SES email identities

4. **Post-Deployment**:
   - Verify SES email address
   - Upload portfolio YAML files to S3 artifacts bucket (optional)
   - Monitor first scheduled execution via CloudWatch Logs

### Cost Estimation

For light usage (daily runs processing ~500 stocks):

- **Lambda**: ~$0.50/month (with Free Tier)
- **DynamoDB**: ~$2/month (with on-demand pricing)
- **S3**: ~$0.50/month (minimal storage)
- **Glue Data Catalog**: First million objects free
- **SNS/SQS**: ~$0.10/month
- **SES**: First 62,000 emails/month free (from Lambda)

**Estimated Total: ~$3-5/month**

*(Costs may vary based on usage patterns and AWS region)*

---

## 🤝 Contributing

Contributions are welcome! This project is open-source and benefits from community improvements.

### How to Contribute

1. **Fork the Repository**

   Click the "Fork" button on GitHub to create your own copy.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/b3stocks.git
   cd b3stocks
   ```

3. **Create a Feature Branch**

   ```bash
   git checkout -b feature/my-awesome-feature
   ```

4. **Make Your Changes**

   - Follow the existing code structure (Clean Architecture)
   - Add docstrings to all functions and classes
   - Use type hints for function parameters and returns
   - Keep functions small and focused (Single Responsibility Principle)

5. **Test Your Changes**

   ```bash
   # Run local tests
   python -m pytest app/tests/
   
   # Deploy to test AWS account
   cd infra
   terraform apply
   ```

6. **Commit Your Changes**

   ```bash
   git add .
   git commit -m "feat: add awesome feature XYZ"
   ```

   Follow [Conventional Commits](https://www.conventionalcommits.org/) style:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `refactor:` for code refactoring
   - `test:` for adding tests

7. **Push to Your Fork**

   ```bash
   git push origin feature/my-awesome-feature
   ```

8. **Open a Pull Request**

   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Provide a clear description of your changes
   - Reference any related issues

### Coding Conventions

- **Python Style**: Follow PEP 8
- **Naming Conventions**:
  - Classes: `PascalCase`
  - Functions/Variables: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
- **Architecture**:
  - Keep domain logic pure (no AWS SDK calls)
  - Use interfaces for all external dependencies
  - Place infrastructure code in `infra/` subdirectories
- **Terraform Style**:
  - Use descriptive resource names
  - Add comments explaining complex configurations
  - Group related resources in the same file

### Branching Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Feature development branches
- `bugfix/*`: Bug fix branches
- `hotfix/*`: Urgent production fixes

### Reporting Issues

Found a bug or have a feature request? [Open an issue](https://github.com/ThiagoPanini/b3stocks/issues) with:

- Clear description of the problem or suggestion
- Steps to reproduce (for bugs)
- Expected vs. actual behavior
- Environment details (Python version, AWS region, etc.)

---

<div align="center">

### ⭐ Star this repository if you find it useful!

**Built with ❤️ by [Thiago Panini](https://github.com/ThiagoPanini)**

[![GitHub](https://img.shields.io/badge/GitHub-ThiagoPanini-181717?style=for-the-badge&logo=github)](https://github.com/ThiagoPanini)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Thiago_Panini-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/thiago-panini)

</div>


