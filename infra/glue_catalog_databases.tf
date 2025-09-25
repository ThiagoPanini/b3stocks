/* -----------------------------------------------------------------------------
  FILE: glue_catalog_databases.tf
  PROJECT: b3stocks

  DESCRIPTION:
    Defines AWS Glue Data Catalog databases for the b3stocks project analytics
    infrastructure. These databases organize tables by data processing stage
    and enable efficient querying and data discovery for analytics workloads.

  DATABASES:
    - db_b3stocks_analytics_cdc: Database for Change Data Capture datasets
    - db_b3stocks_analytics_sor: Database for System of Record (raw/bronze) datasets
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   GLUE DATABASES
   Creating separate databases for different data processing
   stages to organize tables by their data maturity level.
-------------------------------------------------------- */

resource "aws_glue_catalog_database" "b3stocks_analytics_cdc" {
  name        = "db_b3stocks_analytics_cdc"
  description = "Database for CDC datasets on b3stocks project"
}

resource "aws_glue_catalog_database" "b3stocks_analytics_sor" {
  name        = "db_b3stocks_analytics_sor"
  description = "Database for row/raw/bronze datasets on b3stocks project"
}


