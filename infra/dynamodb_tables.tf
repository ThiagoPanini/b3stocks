/* -----------------------------------------------------------------------------
FILE: dynamodb_tables.tf

DESCRIPTION:
  This Terraform handlers the definition of all DynamoDB tables required by
  all app features on b3stocks project.
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   DYNAMODB TABLE: tbl_b3stocks_investment_portfolio
   Defines DynamoDB tables for storing data related to the
   feature of getting data from an user's investment portfolio
-------------------------------------------------------- */

module "aws_dynamodb_table_tbl_b3stocks_investment_portfolio" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/dynamodb-table/v0.4.0"

  name             = "tbl_b3stocks_investment_portfolio"
  hash_key         = "owner_mail"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attributes = [
    {
      name = "owner_mail"
      type = "S"
    }
  ]
}


/* --------------------------------------------------------
   DYNAMODB TABLE: tbl_b3stocks_active_stocks
   Defines DynamoDB tables for storing data related to
   active stocks scrapped from a source website or API.
-------------------------------------------------------- */

module "aws_dynamodb_table_tbl_b3stocks_active_stocks" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/dynamodb-table/v0.4.0"

  name             = "tbl_b3stocks_active_stocks"
  hash_key         = "code"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attributes = [
    {
      name = "code"
      type = "S"
    }
  ]
}

