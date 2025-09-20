/* -----------------------------------------------------------------------------
  FILE: glue_catalog_tables_sor.tf
  PROJECT: b3stocks

  DESCRIPTION:
    Defines AWS Glue Data Catalog tables for System of Record (SoR) datasets
    in the b3stocks project. These tables provide structured access to raw
    and processed data stored in Parquet format in S3, enabling efficient
    analytics and reporting workflows.

  TABLES:
    - sor_tbl_b3stocks_investment_portfolio: SoR data for investment portfolios
    - sor_tbl_b3stocks_active_stocks: SoR data for active B3 stocks
    - sor_tbl_fundamentus_eod_stock_metrics: SoR data for Fundamentus stock metrics
----------------------------------------------------------------------------- */


/* --------------------------------------------------------
   GLUE TABLE: sor_tbl_b3stocks_investment_portfolio
   System of Record table for investment portfolio data
   stored in Parquet format. Partitioned by event_date
   for optimized query performance.
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
      name    = "owner_name"
      type    = "string"
      comment = "Full name of the investment portfolio owner"
    }

    columns {
      name    = "owner_mail"
      type    = "string"
      comment = "Email address of the investment portfolio owner (primary key)"
    }

    columns {
      name    = "stocks"
      type    = "string"
      comment = "JSON string containing the list of stocks in the portfolio"
    }

    columns {
      name    = "source_url"
      type    = "string"
      comment = "URL source where the portfolio data was extracted from"
    }

    columns {
      name    = "created_at"
      type    = "string"
      comment = "Timestamp when the portfolio record was first created"
    }

    columns {
      name    = "updated_at"
      type    = "string"
      comment = "Timestamp when the portfolio record was last updated"
    }
  }

  partition_keys {
    name    = "event_date"
    type    = "string"
    comment = "Date partition in YYYY-MM-DD format for efficient querying"
  }
}


/* --------------------------------------------------------
   GLUE TABLE: sor_tbl_b3stocks_active_stocks
   System of Record table for active B3 stocks data
   stored in Parquet format. Partitioned by event_date
   for optimized query performance.
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
      name    = "code"
      type    = "string"
      comment = "B3 stock ticker symbol (primary key)"
    }

    columns {
      name    = "company_name"
      type    = "string"
      comment = "Official company name associated with the stock"
    }

    columns {
      name    = "request_config"
      type    = "string"
      comment = "Configuration parameters for data extraction requests"
    }

    columns {
      name    = "created_at"
      type    = "string"
      comment = "Timestamp when the stock record was first created"
    }

    columns {
      name    = "updated_at"
      type    = "string"
      comment = "Timestamp when the stock record was last updated"
    }
  }

  partition_keys {
    name    = "event_date"
    type    = "string"
    comment = "Date partition in YYYY-MM-DD format for efficient querying"
  }
}


/* --------------------------------------------------------
   GLUE TABLE: sor_tbl_fundamentus_eod_stock_metrics
   System of Record table for Fundamentus end-of-day stock
   metrics data stored in Parquet format. Contains comprehensive
   financial metrics for B3 stocks. Partitioned by event_date.
-------------------------------------------------------- */

resource "aws_glue_catalog_table" "sor_tbl_fundamentus_eod_stock_metrics" {
  name          = "sor_tbl_fundamentus_eod_stock_metrics"
  database_name = aws_glue_catalog_database.b3stocks_analytics_sor.name
  table_type    = "EXTERNAL_TABLE"

  parameters = {
    classification = "parquet"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.analytics_sor.bucket}/sor_tbl_fundamentus_eod_stock_metrics/"
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
      name    = "nome_papel"
      type    = "string"
      comment = "Stock ticker symbol on B3"
    }

    columns {
      name    = "tipo_papel"
      type    = "string"
      comment = "Stock type (ON = common, PN = preferred, etc.)"
    }

    columns {
      name    = "nome_empresa"
      type    = "string"
      comment = "Company's commercial name"
    }

    columns {
      name    = "nome_setor"
      type    = "string"
      comment = "Company's sector classification"
    }

    columns {
      name    = "nome_subsetor"
      type    = "string"
      comment = "Company's subsector classification"
    }

    columns {
      name    = "vlr_cot"
      type    = "string"
      comment = "Current stock price"
    }

    columns {
      name    = "dt_ult_cot"
      type    = "string"
      comment = "Date of last trading session"
    }

    columns {
      name    = "vlr_cot_min_52_sem"
      type    = "string"
      comment = "52-week low price"
    }

    columns {
      name    = "vlr_cot_max_52_sem"
      type    = "string"
      comment = "52-week high price"
    }

    columns {
      name    = "vol_med_neg_2m"
      type    = "string"
      comment = "Average trading volume in last 2 months"
    }

    columns {
      name    = "vlr_mercado"
      type    = "string"
      comment = "Market value of the company"
    }

    columns {
      name    = "vlr_firma"
      type    = "string"
      comment = "Enterprise value (market value + net debt)"
    }

    columns {
      name    = "dt_ult_balanco_proc"
      type    = "string"
      comment = "Date of last processed balance sheet"
    }

    columns {
      name    = "num_acoes"
      type    = "string"
      comment = "Total number of shares"
    }

    columns {
      name    = "pct_var_dia"
      type    = "string"
      comment = "Daily price variation percentage"
    }

    columns {
      name    = "pct_var_mes"
      type    = "string"
      comment = "Monthly price variation percentage"
    }

    columns {
      name    = "pct_var_30d"
      type    = "string"
      comment = "30-day price variation percentage"
    }

    columns {
      name    = "pct_var_12m"
      type    = "string"
      comment = "12-month price variation percentage"
    }

    columns {
      name    = "pct_var_ano_a0"
      type    = "string"
      comment = "Current year price variation percentage"
    }

    columns {
      name    = "pct_var_ano_a1"
      type    = "string"
      comment = "Previous year price variation percentage"
    }

    columns {
      name    = "pct_var_ano_a2"
      type    = "string"
      comment = "Two years ago price variation percentage"
    }

    columns {
      name    = "pct_var_ano_a3"
      type    = "string"
      comment = "Three years ago price variation percentage"
    }

    columns {
      name    = "pct_var_ano_a4"
      type    = "string"
      comment = "Four years ago price variation percentage"
    }

    columns {
      name    = "pct_var_ano_a5"
      type    = "string"
      comment = "Five years ago price variation percentage"
    }

    columns {
      name    = "vlr_p_sobre_l"
      type    = "string"
      comment = "Price-to-Earnings ratio (P/E)"
    }

    columns {
      name    = "vlr_p_sobre_vp"
      type    = "string"
      comment = "Price-to-Book ratio (P/B)"
    }

    columns {
      name    = "vlr_p_sobre_ebit"
      type    = "string"
      comment = "Price-to-EBIT ratio"
    }

    columns {
      name    = "vlr_psr"
      type    = "string"
      comment = "Price-to-Sales ratio (PSR)"
    }

    columns {
      name    = "vlr_p_sobre_ativ"
      type    = "string"
      comment = "Price-to-Assets ratio"
    }

    columns {
      name    = "vlr_p_sobre_cap_giro"
      type    = "string"
      comment = "Price-to-Working Capital ratio"
    }

    columns {
      name    = "vlr_p_sobre_ativ_circ_liq"
      type    = "string"
      comment = "Price-to-Net Current Assets ratio"
    }

    columns {
      name    = "vlr_div_yield"
      type    = "string"
      comment = "Dividend yield percentage"
    }

    columns {
      name    = "vlr_ev_sobre_ebitda"
      type    = "string"
      comment = "Enterprise Value to EBITDA ratio"
    }

    columns {
      name    = "vlr_ev_sobre_ebit"
      type    = "string"
      comment = "Enterprise Value to EBIT ratio"
    }

    columns {
      name    = "pct_cresc_rec_liq_ult_5a"
      type    = "string"
      comment = "5-year net revenue growth percentage"
    }

    columns {
      name    = "vlr_lpa"
      type    = "string"
      comment = "Earnings per share (EPS)"
    }

    columns {
      name    = "vlr_vpa"
      type    = "string"
      comment = "Book value per share"
    }

    columns {
      name    = "vlr_margem_bruta"
      type    = "string"
      comment = "Gross margin percentage"
    }

    columns {
      name    = "vlr_margem_ebit"
      type    = "string"
      comment = "EBIT margin percentage"
    }

    columns {
      name    = "vlr_margem_liq"
      type    = "string"
      comment = "Net margin percentage"
    }

    columns {
      name    = "vlr_ebit_sobre_ativo"
      type    = "string"
      comment = "EBIT over assets ratio"
    }

    columns {
      name    = "vlr_roic"
      type    = "string"
      comment = "Return on invested capital (ROIC)"
    }

    columns {
      name    = "vlr_roe"
      type    = "string"
      comment = "Return on equity (ROE)"
    }

    columns {
      name    = "vlr_liquidez_corr"
      type    = "string"
      comment = "Current liquidity ratio"
    }

    columns {
      name    = "vlr_divida_bruta_sobre_patrim"
      type    = "string"
      comment = "Gross debt to equity ratio"
    }

    columns {
      name    = "vlr_giro_ativos"
      type    = "string"
      comment = "Asset turnover ratio"
    }

    columns {
      name    = "vlr_ativo"
      type    = "string"
      comment = "Total assets value"
    }

    columns {
      name    = "vlr_disponibilidades"
      type    = "string"
      comment = "Cash and cash equivalents"
    }

    columns {
      name    = "vlr_ativ_circulante"
      type    = "string"
      comment = "Current assets value"
    }

    columns {
      name    = "vlr_divida_bruta"
      type    = "string"
      comment = "Gross debt value"
    }

    columns {
      name    = "vlr_divida_liq"
      type    = "string"
      comment = "Net debt value"
    }

    columns {
      name    = "vlr_patrim_liq"
      type    = "string"
      comment = "Shareholders' equity value"
    }

    columns {
      name    = "vlr_receita_liq_ult_12m"
      type    = "string"
      comment = "Net revenue in last 12 months"
    }

    columns {
      name    = "vlr_ebit_ult_12m"
      type    = "string"
      comment = "EBIT in last 12 months"
    }

    columns {
      name    = "vlr_lucro_liq_ult_12m"
      type    = "string"
      comment = "Net income in last 12 months"
    }

    columns {
      name    = "vlr_receita_liq_ult_3m"
      type    = "string"
      comment = "Net revenue in last 3 months"
    }

    columns {
      name    = "vlr_ebit_ult_3m"
      type    = "string"
      comment = "EBIT in last 3 months"
    }

    columns {
      name    = "vlr_lucro_liq_ult_3m"
      type    = "string"
      comment = "Net income in last 3 months"
    }
  }

  partition_keys {
    name    = "execution_date"
    type    = "string"
    comment = "Date reference for data extraction"
  }
}
