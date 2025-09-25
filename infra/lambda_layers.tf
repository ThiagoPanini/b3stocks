/* -----------------------------------------------------------------------------
FILE: lambda_layers.tf
PROJECT: b3stocks

DESCRIPTION:
  This Terraform file defines AWS Lambda layers for the b3stocks project.
  Layers provide shared dependencies and libraries that can be reused across
  multiple Lambda functions, reducing deployment package sizes and enabling
  consistent dependency management.

LAYERS:
  - b3stocks-deps: Core dependencies including PynamoDB, PyYAML, requests,
    BeautifulSoup4, and lxml for AWS service interaction and web scraping
----------------------------------------------------------------------------- */

module "aws_lambda_layers" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-layer/v0.6.0"

  layers_config = [
    {
      name = "b3stocks-deps"
      requirements = [
        "pynamodb==6.1.0",
        "PyYAML==6.0.2",
        "requests==2.32.3",
        "beautifulsoup4==4.13.3",
        "lxml==5.3.1"
      ],
      runtime     = ["python3.12", "python3.13"]
      description = "Dependencies for b3stocks project, including useful packages to extract investment data and interact with AWS services"
    }
  ]
}

