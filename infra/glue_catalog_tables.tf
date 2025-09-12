/* -----------------------------------------------------------------------------
  FILE: glue_catalog_tables.tf

  DESCRIPTION:
    Defines Glue Data Catalog database and table for DynamoDB investment portfolio
    CDC data landed in S3.
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   GLUE DATABASES
   Defining databases for analytics use cases.
-------------------------------------------------------- */

resource "aws_glue_catalog_database" "b3stocks_analytics_cdc" {
  name        = "db_b3stocks_analytics_cdc"
  description = "Database for CDC datasets on b3stocks project"
}


/* --------------------------------------------------------
   GLUE TABLE: tbl_cdc_brstocks_investment_portfolio
   CDC table for sharing investment portfolio data taken from
   DynamoDB stream and landed in S3.
-------------------------------------------------------- */

resource "aws_glue_catalog_table" "tbl_cdc_brstocks_investment_portfolio" {
  name          = "tbl_cdc_brstocks_investment_portfolio"
  database_name = aws_glue_catalog_database.b3stocks_analytics_cdc.name
  table_type    = "EXTERNAL_TABLE"

  parameters = {
    classification = "json"
  }

  storage_descriptor {
    location          = "s3://${aws_s3_bucket.analytics_cdc.bucket}/dynamodb/tbl_brstocks_investment_portfolio/"
    input_format      = "org.apache.hadoop.mapred.TextInputFormat"
    output_format     = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"
    number_of_buckets = -1

    ser_de_info {
      name                  = "json"
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"
      parameters = {
        "ignore.malformed.json" = "true"
      }
    }

    columns {
      name = "table_name"
      type = "string"
    }

    columns {
      name = "event_id"
      type = "string"
    }

    columns {
      name = "event_name"
      type = "string"
    }

    columns {
      name = "event_version"
      type = "string"
    }

    columns {
      name = "event_source"
      type = "string"
    }

    columns {
      name = "aws_region"
      type = "string"
    }

    columns {
      name = "table_keys"
      type = "struct<owner_mail:string>"
    }

    columns {
      name = "table_new_image"
      type = "struct<owner_name:string,updated_at:string,owner_mail:string,created_at:string,source_url:string,stocks:string>"
    }

    columns {
      name = "table_old_image"
      type = "struct<owner_name:string,updated_at:string,owner_mail:string,created_at:string,source_url:string,stocks:string>"
    }

    columns {
      name = "size_bytes"
      type = "integer"
    }

    columns {
      name = "stream_view_type"
      type = "string"
    }

    columns {
      name = "event_source_arn"
      type = "string"
    }
  }

  partition_keys {
    name = "event_date"
    type = "string"
  }
}
