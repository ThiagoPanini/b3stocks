/* -----------------------------------------------------------------------------
FILE: dynamodb_tables.tf

DESCRIPTION:
  This Terraform handlers the definition of all DynamoDB tables required by
  all app features on b3stocks project.

RESOURCES:
  - module.aws_dynamodb_table_tbl_brstocks_investment_portfolio:
        Deploys a DynamoDB table using the tfbox module with configurable
        properties such as name, hash key, range key, and attributes.
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   DYNAMODB TABLE: get-investment-portfolio
   Defines DynamoDB tables for storing data related to the
   feature of getting data from an user's investment portfolio
-------------------------------------------------------- */

module "aws_dynamodb_table_tbl_brstocks_investment_portfolio" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/dynamodb-table/v0.1.2"

  name     = "tbl_brstocks_investment_portfolio"
  hash_key = "owner_mail"

  attributes = [
    {
      name = "owner_mail"
      type = "S"
    }
  ]
}
