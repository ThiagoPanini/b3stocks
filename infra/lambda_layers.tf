/* -----------------------------------------------------------------------------
FILE: lambda_layers.tf

DESCRIPTION:
  This Terraform file centralizes the definition of all AWS Lambda layers used
  along the b3stocks project.
----------------------------------------------------------------------------- */

module "aws_lambda_layers" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-layer/v0.4.0"

  layers_map = {
    pynamodb_6_1_0 = {
      requirements = [
        "pynamodb==6.1.0",
      ]
      runtime     = "python3.12"
      description = "Pynamodb package and its dependencies to interact with DynamoDB from AWS Lambda"
    }
  }
}

