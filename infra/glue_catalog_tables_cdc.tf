/* -----------------------------------------------------------------------------
  FILE: glue_catalog_tables_cdc.tf
  PROJECT: b3stocks

  DESCRIPTION:
    Defines AWS Glue Data Catalog tables for Change Data Capture (CDC) datasets
    in the b3stocks project. These tables provide a structured view of data
    streamed from DynamoDB tables and landed in S3, enabling analytics and
    monitoring of data changes over time.

  TABLES:
    - cdc_tbl_b3stocks_investment_portfolio: CDC data for investment portfolios
    - cdc_tbl_b3stocks_active_stocks: CDC data for active B3 stocks
----------------------------------------------------------------------------- */


/* --------------------------------------------------------
   GLUE TABLE: cdc_tbl_b3stocks_investment_portfolio
   CDC table containing investment portfolio change events
   captured from DynamoDB Streams and stored in S3 as JSON.
   Partitioned by event_date for efficient querying.
-------------------------------------------------------- */

resource "aws_glue_catalog_table" "cdc_tbl_b3stocks_investment_portfolio" {
  name          = "cdc_tbl_b3stocks_investment_portfolio"
  database_name = aws_glue_catalog_database.b3stocks_analytics_cdc.name
  table_type    = "EXTERNAL_TABLE"

  parameters = {
    classification = "json"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.analytics_cdc.bucket}/dynamodb/cdc_tbl_b3stocks_investment_portfolio/"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"

    ser_de_info {
      name                  = "json"
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"
    }

    columns {
      name    = "table_name"
      type    = "string"
      comment = "Source DynamoDB table name that generated the CDC event"
    }

    columns {
      name    = "event_id"
      type    = "string"
      comment = "Unique identifier for the DynamoDB stream event"
    }

    columns {
      name    = "event_name"
      type    = "string"
      comment = "Type of DynamoDB operation (INSERT, MODIFY, REMOVE)"
    }

    columns {
      name    = "event_version"
      type    = "string"
      comment = "DynamoDB Streams event version number"
    }

    columns {
      name    = "event_source"
      type    = "string"
      comment = "Source service that generated the event (aws:dynamodb)"
    }

    columns {
      name    = "aws_region"
      type    = "string"
      comment = "AWS region where the DynamoDB table is located"
    }

    columns {
      name    = "table_keys"
      type    = "struct<owner_mail:string>"
      comment = "Primary key values of the affected investment portfolio record"
    }

    columns {
      name    = "table_new_image"
      type    = "string"
      comment = "JSON representation of the item after modification"
    }

    columns {
      name    = "table_old_image"
      type    = "string"
      comment = "JSON representation of the item before modification"
    }

    columns {
      name    = "size_bytes"
      type    = "bigint"
      comment = "Size of the DynamoDB stream record in bytes"
    }

    columns {
      name    = "stream_view_type"
      type    = "string"
      comment = "DynamoDB stream view type (NEW_AND_OLD_IMAGES, KEYS_ONLY, etc.)"
    }

    columns {
      name    = "event_source_arn"
      type    = "string"
      comment = "ARN of the DynamoDB stream that generated the event"
    }
  }

  partition_keys {
    name    = "event_date"
    type    = "string"
    comment = "Date partition in YYYYMMDD format for efficient querying"
  }
}


/* --------------------------------------------------------
   GLUE TABLE: cdc_tbl_b3stocks_active_stocks
   CDC table containing active stocks change events captured
   from DynamoDB Streams and stored in S3 as JSON.
   Partitioned by event_date for efficient querying.
-------------------------------------------------------- */

resource "aws_glue_catalog_table" "cdc_tbl_b3stocks_active_stocks" {
  name          = "cdc_tbl_b3stocks_active_stocks"
  database_name = aws_glue_catalog_database.b3stocks_analytics_cdc.name
  table_type    = "EXTERNAL_TABLE"

  parameters = {
    classification = "json"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.analytics_cdc.bucket}/dynamodb/cdc_tbl_b3stocks_active_stocks/"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"

    ser_de_info {
      name                  = "json"
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"
    }

    columns {
      name    = "table_name"
      type    = "string"
      comment = "Source DynamoDB table name that generated the CDC event"
    }

    columns {
      name    = "event_id"
      type    = "string"
      comment = "Unique identifier for the DynamoDB stream event"
    }

    columns {
      name    = "event_name"
      type    = "string"
      comment = "Type of DynamoDB operation (INSERT, MODIFY, REMOVE)"
    }

    columns {
      name    = "event_version"
      type    = "string"
      comment = "DynamoDB Streams event version number"
    }

    columns {
      name    = "event_source"
      type    = "string"
      comment = "Source service that generated the event (aws:dynamodb)"
    }

    columns {
      name    = "aws_region"
      type    = "string"
      comment = "AWS region where the DynamoDB table is located"
    }

    columns {
      name    = "table_keys"
      type    = "struct<code:string>"
      comment = "Primary key values of the affected active stock record"
    }

    columns {
      name    = "table_new_image"
      type    = "string"
      comment = "JSON representation of the stock item after modification"
    }

    columns {
      name    = "table_old_image"
      type    = "string"
      comment = "JSON representation of the stock item before modification"
    }

    columns {
      name    = "size_bytes"
      type    = "bigint"
      comment = "Size of the DynamoDB stream record in bytes"
    }

    columns {
      name    = "stream_view_type"
      type    = "string"
      comment = "DynamoDB stream view type (NEW_AND_OLD_IMAGES, KEYS_ONLY, etc.)"
    }

    columns {
      name    = "event_source_arn"
      type    = "string"
      comment = "ARN of the DynamoDB stream that generated the event"
    }
  }

  partition_keys {
    name    = "event_date"
    type    = "string"
    comment = "Date partition in YYYYMMDD format for efficient querying"
  }
}
