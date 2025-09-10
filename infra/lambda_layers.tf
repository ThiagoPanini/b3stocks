/* -----------------------------------------------------------------------------
FILE: lambda_layers.tf

DESCRIPTION:
  This Terraform file centralizes the definition of all AWS Lambda layers used
  along the b3stocks project.
----------------------------------------------------------------------------- */

module "aws_lambda_layers" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-layer/v0.5.0"

  layers_config = [
    {
      name = "pynamodb-and-pyyaml"
      requirements = [
        "pynamodb==6.1.0",
        "PyYAML==6.0.2",
      ],
      runtime     = ["python3.12", "python3.13"]
      description = "Layer with pynamodb v6.1.0 and PyYAML v6.0.2 packages"
    }
  ]
}

