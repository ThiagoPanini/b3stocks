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

resource "aws_glue_catalog_database" "b3stocks_analytics_sor" {
  name        = "db_b3stocks_analytics_sor"
  description = "Database for row/raw/bronze datasets on b3stocks project"
}


