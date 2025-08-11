<div align="center">
    <br><img src="https://github.com/ThiagoPanini/tf-modules-showcase/blob/feature/repo-setup/docs/imgs/logo-b3stocks.png?raw=true" width=200 alt="b3stocks-logo">
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

# b3stocks: Serverless Data Pipeline

Serverless data pipeline to extract active B3 (Brazilian Stock Exchange) stock tickers from the web and publish them to AWS services on a schedule.

This repo contains:
- Python application code that scrapes tickers from Fundamentus, parses them with BeautifulSoup, and publishes messages to an SNS topic
- Infrastructure-as-code (Terraform) to deploy an AWS Lambda with a scheduled EventBridge trigger, IAM role/policies, and an S3 bucket for data landing


## Highlights

- Scrapes active tickers from a public financial website (Fundamentus)
- Robust HTTP client with retries and timeouts
- HTML parsing with BeautifulSoup into typed domain entities
- Publishes messages to Amazon SNS for downstream decoupled consumption
- EventBridge schedule to run the Lambda automatically
- Terraform-managed infra, IAM least-privilege templates, and Lambda layers


## Architecture (overview)

Flow: EventBridge schedule → Lambda → HTTP request to Fundamentus → parse HTML → build domain entities → publish messages to SNS → optional data landing to S3 (IAM policy is in place; writing logic may be added).

You can view or edit the diagram source at `docs/architecture/architecture.drawio`.


## Repository structure

```
app/
	src/
		features/
			cross/               # Shared cross-cutting concerns
				domain/            # HTTP entities, retry config, interfaces
				infra/             # Requests HTTP adapter
				utils/             # Logging, decorators, timing
				value_objects/     # Shared enums/value objects (e.g., InvestmentWebSite)
			get_b3_stock_tickers/
				domain/            # Entities (B3StockTicker), DTOs (OutputDTO), interfaces
				infra/             # Adapters: HTML parser (Fundamentus), SNS topic adapter, mappers
				presentation/      # Lambda handler + HTTPResponseMapper
				use_case/          # GetB3StockTickersUseCase
	tests/
		local/run_local.py     # Simple local runner wiring the Lambda handler

infra/
	get-b3-stock-tickers/    # Terraform module for Lambda + schedule + IAM + S3
		assets/iam/            # Trust and permission policy templates

.github/workflows/ci-feature.yml  # Bot to open PRs from feature/* to main
requirements.txt                  # Application dependencies
LICENSE                           # MIT
```


## Tech stack

- Language: Python 3.12
- Runtime: AWS Lambda
- AWS services: EventBridge, SNS, IAM, S3, CloudWatch Logs
- Libraries: requests, beautifulsoup4, boto3, pydantic (foundation for typing/validation)
- IaC: Terraform >= 1.9 (AWS provider ~> 5.50)


## How it works (code walkthrough)

- Handler: `app.src.features.get_b3_stock_tickers.presentation.get_b3_stock_tickers_presentation.handler`
- Use case: `GetB3StockTickersUseCase`
	- Builds an HTTP request to `https://www.fundamentus.com.br/resultado.php` with a retry-enabled client
	- Parses the HTML with `FundamentusHTMLParserAdapter` into `B3StockTicker` entities:
		- `code` (ticker)
		- `company_name`
		- `date_extracted` (UTC date, YYYY-MM-DD)
	- Adapts into message bodies and batch-publishes them to SNS via `SNSTopicAdapter`
	- Returns an `OutputDTO` with metadata like the number of tickers and the SNS topic name
- Presentation layer maps the result to an HTTP-style response with `HTTPResponseMapper`

Example handler response body (on success):

```json
{
	"success": true,
	"data": {
		"total_tickers": 100,
		"sns_topic_name": "techplay-b3-stock-tickers-topic"
	},
	"error": null
}
```

Notes
- SNS topic publishing requires that the topic exists and that credentials allow `sns:Publish` to it.
- The IAM policy template also grants `s3:PutObject` to a bucket/prefix; writing logic to S3 can be added later.


## Prerequisites

- Python 3.12
- An AWS account with credentials configured locally (e.g., via `aws configure` or env vars)
	- The Lambda publishes to SNS and writes logs to CloudWatch
	- For local runs that touch AWS, ensure your default region and permissions are set
- Terraform >= 1.9 (for deployment)


## Environment variables

Application expects the following environment variables at runtime (Lambda or local):

- `SNS_B3_STOCK_TICKERS_TOPIC_NAME` (required): Name of the SNS topic that receives ticker messages
- `AWS_REGION` or `AWS_DEFAULT_REGION` (recommended for local): Region for AWS SDK calls

Terraform also parameterizes resources via variables (see `infra/get-b3-stock-tickers/variables.tf`):

- `lambda_function_name` (default: `get-b3-stock-tickers`)
- `lambda_function_runtime` (default: `python3.12`)
- `lambda_function_architectures` (default: `["x86_64"]`)
- `lambda_function_timeout_seconds` (default: `180`)
- `lambda_function_cron_expression` (default schedule: daily at 21:00 UTC)
- `s3_bucket_name_prefix` (default: `b3stocks-bronze`); full bucket name becomes `{prefix}-{account_id}-{region}`
- `glue_table_name` (default: `tbl_dim_active_stock_tickers`); used as an S3 prefix in IAM policy
- `sns_topic_name` (default: `techplay-b3-stock-tickers-topic`)
- `sns_topic_display_name` (default: `B3 Stock Tickers Topic`)
- `tags` (default: `{ Project = "tech-playground" }`)


## Run locally

1) Create a virtual environment and install dependencies

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Optional: needed by the local runner to load .env files
pip install python-dotenv
```

2) Create a `.env` file in the repo root (or export env vars in your shell)

```
SNS_B3_STOCK_TICKERS_TOPIC_NAME=techplay-b3-stock-tickers-topic
AWS_DEFAULT_REGION=us-east-1
```

3) Ensure your AWS credentials are available locally (env vars or `~/.aws` config)

4) Run the local script that wires the Lambda handler

```bash
python app/tests/local/run_local.py
```

You should see an HTTP-like response printed with `statusCode`, `headers`, and `body` containing the `OutputDTO` JSON.


## Deploy with Terraform

Infrastructure lives under `infra/get-b3-stock-tickers/` and provisions:
- Lambda function with a scheduled EventBridge rule
- IAM role with policy templates for CloudWatch Logs, SNS publish, and S3 put
- S3 bucket (private) with public access blocked
- Lambda Layer built from the app’s core dependencies

Important
- The SNS topic itself is referenced by name but not created by this stack as-is. Ensure the topic exists in the target account/region, or extend the stack with a topic module.

Typical workflow

```bash
cd infra/get-b3-stock-tickers
terraform init
terraform plan -out tfplan \
	-var "sns_topic_name=techplay-b3-stock-tickers-topic" \
	-var "s3_bucket_name_prefix=b3stocks-bronze"
terraform apply tfplan
```

After apply
- Lambda name defaults to `get-b3-stock-tickers`
- The function handler is `app.src.features.get_b3_stock_tickers.presentation.get_b3_stock_tickers_presentation.handler`
- An EventBridge schedule triggers the function (default daily at 21:00 UTC)
- Check CloudWatch Logs for execution output


## Domain model and contracts

- Entity: `B3StockTicker`
	- `code: str` (uppercased)
	- `company_name: str` (uppercased)
	- `date_extracted: str` (UTC date, `YYYY-MM-DD`)

- Message body (published to SNS)
	- `{ code, company_name, date_extracted }`

- Output DTO (application response contract)
	- `success: bool`
	- `data: any` (on success; e.g., `{ total_tickers, sns_topic_name }`)
	- `error: str | null` (on failure)


## CI/CD

- A lightweight CI workflow `.github/workflows/ci-feature.yml` opens a PR from any `feature/*` branch to `main` automatically using a bot action
- Use feature branches and push to trigger the PR creation


## Notes on extensibility

- The IAM policy already grants `s3:PutObject` to a path controlled by `glue_table_name`; add an S3 writer adapter and repository if you want the Lambda to persist raw/bronze data
- Add consumers (SQS, Lambda, etc.) subscribed to the SNS topic to fan out processing
- Consider rate limiting and backoff strategies if the source website changes or throttles


## Troubleshooting

- SNS publish errors: verify `SNS_B3_STOCK_TICKERS_TOPIC_NAME`, AWS credentials, and that the topic exists in the same region
- Region/endpoint errors: set `AWS_DEFAULT_REGION` or `AWS_REGION` locally, and ensure your AWS profile matches the target region
- HTML parsing errors: websites change; inspect the DOM and update `FundamentusHTMLParserAdapter` selectors accordingly
- Local `.env` not loaded: install `python-dotenv` and ensure `app/tests/local/run_local.py` can find your `.env`


## Legal and scraping ethics

Scrape responsibly. Check the source website’s terms of service and robots.txt. Respect rate limits, caching opportunities, and only collect what you need.


## License

This project is licensed under the MIT License — see `LICENSE` for details.

