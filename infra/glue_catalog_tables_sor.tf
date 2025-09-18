/* -----------------------------------------------------------------------------
  FILE: glue_catalog_tables_sor.tf

  DESCRIPTION:
    Defines Glue Data Catalog tables for system of record (SoR) data landed in
    S3.
----------------------------------------------------------------------------- */


/* --------------------------------------------------------
   GLUE TABLE: sor_tbl_b3stocks_investment_portfolio
   SoR table for sharing investment portfolio data taken from
   DynamoDB stream and landed in S3.
-------------------------------------------------------- */

resource "aws_glue_catalog_table" "sor_tbl_b3stocks_investment_portfolio" {
  name          = "sor_tbl_b3stocks_investment_portfolio"
  database_name = aws_glue_catalog_database.b3stocks_analytics_sor.name
  table_type    = "EXTERNAL_TABLE"

  parameters = {
    classification = "parquet"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.analytics_sor.bucket}/sor_tbl_b3stocks_investment_portfolio/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      name                  = "parquet"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = 1
      }
    }

    columns {
      name = "owner_name"
      type = "string"
    }

    columns {
      name = "owner_mail"
      type = "string"
    }

    columns {
      name = "stocks"
      type = "string"
    }

    columns {
      name = "source_url"
      type = "string"
    }

    columns {
      name = "created_at"
      type = "string"
    }

    columns {
      name = "updated_at"
      type = "string"
    }
  }

  partition_keys {
    name = "event_date"
    type = "string"
  }
}


/* --------------------------------------------------------
   GLUE TABLE: sor_tbl_b3stocks_active_stocks
   SoR table for raw data on active stocks landed in S3.
-------------------------------------------------------- */

resource "aws_glue_catalog_table" "sor_tbl_b3stocks_active_stocks" {
  name          = "sor_tbl_b3stocks_active_stocks"
  database_name = aws_glue_catalog_database.b3stocks_analytics_sor.name
  table_type    = "EXTERNAL_TABLE"

  parameters = {
    classification = "parquet"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.analytics_sor.bucket}/sor_tbl_b3stocks_active_stocks/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      name                  = "parquet"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = 1
      }
    }

    columns {
      name = "code"
      type = "string"
    }

    columns {
      name = "company_name"
      type = "string"
    }

    columns {
      name = "request_config"
      type = "string"
    }

    columns {
      name = "created_at"
      type = "string"
    }

    columns {
      name = "updated_at"
      type = "string"
    }
  }

  partition_keys {
    name = "event_date"
    type = "string"
  }
}
