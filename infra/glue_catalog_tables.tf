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

resource "aws_glue_catalog_database" "b3stocks_analytics_bronze" {
  name        = "db_b3stocks_analytics_bronze"
  description = "Database for bronze layer analytics datasets on b3stocks project"
}


/* --------------------------------------------------------
   GLUE TABLE: tbsor_brstocks_investment_portfolio
   Bronze table for storing a plain JSON representation of
   the investment portfolio data landed from DynamoDB streams.
-------------------------------------------------------- */

resource "aws_glue_catalog_table" "tbl_cdc_brstocks_investment_portfolio" {
  name          = "tbl_cdc_brstocks_investment_portfolio"
  database_name = aws_glue_catalog_database.b3stocks_analytics_bronze.name
  table_type    = "EXTERNAL_TABLE"

  parameters = {
    classification = "json"
  }

  storage_descriptor {
    location          = "s3://${aws_s3_bucket.analytics_bronze.bucket}/raw/dynamodb/tbl_brstocks_investment_portfolio/"
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
      name = "table"
      type = "string"
    }

    columns {
      name = "event_type"
      type = "string"
    }

    columns {
      name = "event_ts"
      type = "string"
    }

    columns {
      name = "sequence_number"
      type = "string"
    }

    columns {
      name = "keys"
      type = "struct<owner_mail:string>"
    }

    columns {
      name = "new_image"
      type = "struct<owner_name:string,updated_at:string,owner_mail:string,created_at:string,source_url:string,stocks:string>"
    }

    columns {
      name = "old_image"
      type = "struct<owner_name:string,updated_at:string,owner_mail:string,created_at:string,source_url:string,stocks:string>"
    }

    columns {
      name = "source_region"
      type = "string"
    }

    columns {
      name = "is_deleted"
      type = "boolean"
    }
  }

  # Partitioning strategy: partition data by ingest_date=YYYY-MM-DD
  # S3 layout expected: s3://<bucket>/raw/dynamodb/tbl_brstocks_investment_portfolio/ingest_date=2025-09-10/...
  partition_keys {
    name = "ingest_date"
    type = "string"
  }

}
