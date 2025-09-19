/* -----------------------------------------------------------------------------
FILE: dynamodb_tables.tf
PROJECT: b3stocks

DESCRIPTION:
  This Terraform file defines all DynamoDB tables required by the b3stocks
  project features. Each table is configured with appropriate attributes,
  streaming capabilities, and partition keys to support the application's
  data storage and CDC (Change Data Capture) requirements.

TABLES:
  - tbl_b3stocks_investment_portfolio: Stores user investment portfolio data
  - tbl_b3stocks_active_stocks: Stores active B3 stock information
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   DYNAMODB TABLE: tbl_b3stocks_investment_portfolio
   Stores user investment portfolio data with owner email
   as partition key. Enables DynamoDB Streams for CDC
   processing to capture portfolio changes and updates.
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
   Stores active stock data scraped from B3 sources with
   stock code as partition key. Enables DynamoDB Streams
   for CDC processing to track stock data changes.
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

