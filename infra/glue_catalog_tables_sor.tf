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
      name    = "stock_ticker"
      type    = "string"
      comment = "Stock ticker symbol on B3"
    }

    columns {
      name    = "stock_type"
      type    = "string"
      comment = "Stock type (ON = common, PN = preferred, etc.)"
    }

    columns {
      name    = "company_name"
      type    = "string"
      comment = "Company's commercial name"
    }

    columns {
      name    = "sector_name"
      type    = "string"
      comment = "Company's sector classification"
    }

    columns {
      name    = "subsector_name"
      type    = "string"
      comment = "Company's subsector classification"
    }

    columns {
      name    = "stock_price"
      type    = "string"
      comment = "Current stock price"
    }

    columns {
      name    = "last_trading_date"
      type    = "string"
      comment = "Date of last trading session"
    }

    columns {
      name    = "min_52_week_price"
      type    = "string"
      comment = "52-week low price"
    }

    columns {
      name    = "max_52_week_price"
      type    = "string"
      comment = "52-week high price"
    }

    columns {
      name    = "avg_trading_volume_2m"
      type    = "string"
      comment = "Average trading volume in last 2 months"
    }

    columns {
      name    = "market_value"
      type    = "string"
      comment = "Market value of the company"
    }

    columns {
      name    = "enterprise_value"
      type    = "string"
      comment = "Enterprise value (market value + net debt)"
    }

    columns {
      name    = "last_balance_sheet_date"
      type    = "string"
      comment = "Date of last processed balance sheet"
    }

    columns {
      name    = "total_shares"
      type    = "string"
      comment = "Total number of shares"
    }

    columns {
      name    = "daily_variation_pct"
      type    = "string"
      comment = "Daily price variation percentage"
    }

    columns {
      name    = "monthly_variation_pct"
      type    = "string"
      comment = "Monthly price variation percentage"
    }

    columns {
      name    = "variation_30d_pct"
      type    = "string"
      comment = "30-day price variation percentage"
    }

    columns {
      name    = "variation_12m_pct"
      type    = "string"
      comment = "12-month price variation percentage"
    }

    columns {
      name    = "current_year_variation_pct"
      type    = "string"
      comment = "Current year price variation percentage"
    }

    columns {
      name    = "year_minus_1_variation_pct"
      type    = "string"
      comment = "Previous year price variation percentage"
    }

    columns {
      name    = "year_minus_2_variation_pct"
      type    = "string"
      comment = "Two years ago price variation percentage"
    }

    columns {
      name    = "year_minus_3_variation_pct"
      type    = "string"
      comment = "Three years ago price variation percentage"
    }

    columns {
      name    = "year_minus_4_variation_pct"
      type    = "string"
      comment = "Four years ago price variation percentage"
    }

    columns {
      name    = "year_minus_5_variation_pct"
      type    = "string"
      comment = "Five years ago price variation percentage"
    }

    columns {
      name    = "price_to_earnings_ratio"
      type    = "string"
      comment = "Price-to-Earnings ratio (P/E)"
    }

    columns {
      name    = "price_to_book_ratio"
      type    = "string"
      comment = "Price-to-Book ratio (P/B)"
    }

    columns {
      name    = "price_to_ebit_ratio"
      type    = "string"
      comment = "Price-to-EBIT ratio"
    }

    columns {
      name    = "price_to_sales_ratio"
      type    = "string"
      comment = "Price-to-Sales ratio (PSR)"
    }

    columns {
      name    = "price_to_assets_ratio"
      type    = "string"
      comment = "Price-to-Assets ratio"
    }

    columns {
      name    = "price_to_working_capital_ratio"
      type    = "string"
      comment = "Price-to-Working Capital ratio"
    }

    columns {
      name    = "price_to_net_current_assets_ratio"
      type    = "string"
      comment = "Price-to-Net Current Assets ratio"
    }

    columns {
      name    = "dividend_yield"
      type    = "string"
      comment = "Dividend yield percentage"
    }

    columns {
      name    = "ev_to_ebitda_ratio"
      type    = "string"
      comment = "Enterprise Value to EBITDA ratio"
    }

    columns {
      name    = "ev_to_ebit_ratio"
      type    = "string"
      comment = "Enterprise Value to EBIT ratio"
    }

    columns {
      name    = "net_revenue_5y_growth_pct"
      type    = "string"
      comment = "5-year net revenue growth percentage"
    }

    columns {
      name    = "earnings_per_share"
      type    = "string"
      comment = "Earnings per share (EPS)"
    }

    columns {
      name    = "book_value_per_share"
      type    = "string"
      comment = "Book value per share"
    }

    columns {
      name    = "gross_margin_pct"
      type    = "string"
      comment = "Gross margin percentage"
    }

    columns {
      name    = "ebit_margin_pct"
      type    = "string"
      comment = "EBIT margin percentage"
    }

    columns {
      name    = "net_margin_pct"
      type    = "string"
      comment = "Net margin percentage"
    }

    columns {
      name    = "ebit_to_assets_ratio"
      type    = "string"
      comment = "EBIT over assets ratio"
    }

    columns {
      name    = "return_on_invested_capital"
      type    = "string"
      comment = "Return on invested capital (ROIC)"
    }

    columns {
      name    = "return_on_equity"
      type    = "string"
      comment = "Return on equity (ROE)"
    }

    columns {
      name    = "current_liquidity_ratio"
      type    = "string"
      comment = "Current liquidity ratio"
    }

    columns {
      name    = "gross_debt_to_equity_ratio"
      type    = "string"
      comment = "Gross debt to equity ratio"
    }

    columns {
      name    = "asset_turnover_ratio"
      type    = "string"
      comment = "Asset turnover ratio"
    }

    columns {
      name    = "total_assets"
      type    = "string"
      comment = "Total assets value"
    }

    columns {
      name    = "cash_and_equivalents"
      type    = "string"
      comment = "Cash and cash equivalents"
    }

    columns {
      name    = "current_assets"
      type    = "string"
      comment = "Current assets value"
    }

    columns {
      name    = "gross_debt"
      type    = "string"
      comment = "Gross debt value"
    }

    columns {
      name    = "net_debt"
      type    = "string"
      comment = "Net debt value"
    }

    columns {
      name    = "shareholders_equity"
      type    = "string"
      comment = "Shareholders' equity value"
    }

    columns {
      name    = "net_revenue_12m"
      type    = "string"
      comment = "Net revenue in last 12 months"
    }

    columns {
      name    = "ebit_12m"
      type    = "string"
      comment = "EBIT in last 12 months"
    }

    columns {
      name    = "net_income_12m"
      type    = "string"
      comment = "Net income in last 12 months"
    }

    columns {
      name    = "net_revenue_3m"
      type    = "string"
      comment = "Net revenue in last 3 months"
    }

    columns {
      name    = "ebit_3m"
      type    = "string"
      comment = "EBIT in last 3 months"
    }

    columns {
      name    = "net_income_3m"
      type    = "string"
      comment = "Net income in last 3 months"
    }

    columns {
      name    = "execution_datetime"
      type    = "string"
      comment = "Timestamp of data extraction"
    }
  }

  partition_keys {
    name    = "execution_date"
    type    = "int"
    comment = "Date reference in YYYYMMDD format"
  }
}
