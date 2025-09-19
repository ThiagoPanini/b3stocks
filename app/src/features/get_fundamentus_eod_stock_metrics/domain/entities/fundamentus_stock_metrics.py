from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional


@dataclass
class FundamentusStockMetrics:
    """
    Represents Fundamentus stock metrics data extracted from the Fundamentus website.

    This entity contains comprehensive financial metrics and indicators for stocks
    traded on the Brazilian stock exchange (B3), as scraped from the Fundamentus
    investment analysis platform.

    Attributes:
        stock_ticker (str): Stock ticker symbol on B3
        stock_type (str): Stock type (ON = common, PN = preferred, etc.)
        company_name (str): Company's commercial name
        sector_name (str): Company's sector classification
        subsector_name (str): Company's subsector classification
        stock_price (str): Current stock price
        last_trading_date (str): Date of last trading session
        min_52_week_price (str): 52-week low price
        max_52_week_price (str): 52-week high price
        avg_trading_volume_2m (str): Average trading volume in last 2 months
        market_value (str): Market value of the company
        enterprise_value (str): Enterprise value (market value + net debt)
        last_balance_sheet_date (str): Date of last processed balance sheet
        total_shares (str): Total number of shares
        daily_variation_pct (str): Daily price variation percentage
        monthly_variation_pct (str): Monthly price variation percentage
        variation_30d_pct (str): 30-day price variation percentage
        variation_12m_pct (str): 12-month price variation percentage
        current_year_variation_pct (str): Current year price variation percentage
        year_minus_1_variation_pct (str): Previous year price variation percentage
        year_minus_2_variation_pct (str): Two years ago price variation percentage
        year_minus_3_variation_pct (str): Three years ago price variation percentage
        year_minus_4_variation_pct (str): Four years ago price variation percentage
        year_minus_5_variation_pct (str): Five years ago price variation percentage
        price_to_earnings_ratio (str): Price-to-Earnings ratio (P/E)
        price_to_book_ratio (str): Price-to-Book ratio (P/B)
        price_to_ebit_ratio (str): Price-to-EBIT ratio
        price_to_sales_ratio (str): Price-to-Sales ratio (PSR)
        price_to_assets_ratio (str): Price-to-Assets ratio
        price_to_working_capital_ratio (str): Price-to-Working Capital ratio
        price_to_net_current_assets_ratio (str): Price-to-Net Current Assets ratio
        dividend_yield (str): Dividend yield percentage
        ev_to_ebitda_ratio (str): Enterprise Value to EBITDA ratio
        ev_to_ebit_ratio (str): Enterprise Value to EBIT ratio
        net_revenue_5y_growth_pct (str): 5-year net revenue growth percentage
        earnings_per_share (str): Earnings per share (EPS)
        book_value_per_share (str): Book value per share
        gross_margin_pct (str): Gross margin percentage
        ebit_margin_pct (str): EBIT margin percentage
        net_margin_pct (str): Net margin percentage
        ebit_to_assets_ratio (str): EBIT over assets ratio
        return_on_invested_capital (str): Return on invested capital (ROIC)
        return_on_equity (str): Return on equity (ROE)
        current_liquidity_ratio (str): Current liquidity ratio
        gross_debt_to_equity_ratio (str): Gross debt to equity ratio
        asset_turnover_ratio (str): Asset turnover ratio
        total_assets (str): Total assets value
        cash_and_equivalents (str): Cash and cash equivalents
        current_assets (str): Current assets value
        gross_debt (str): Gross debt value
        net_debt (str): Net debt value
        shareholders_equity (str): Shareholders' equity value
        net_revenue_12m (str): Net revenue in last 12 months
        ebit_12m (str): EBIT in last 12 months
        net_income_12m (str): Net income in last 12 months
        net_revenue_3m (str): Net revenue in last 3 months
        ebit_3m (str): EBIT in last 3 months
        net_income_3m (str): Net income in last 3 months
        execution_datetime (str): Timestamp of data extraction
        execution_date (int): Date reference in YYYYMMDD format
    """

    stock_ticker: str
    stock_type: str
    company_name: str
    sector_name: str
    subsector_name: str
    stock_price: str
    last_trading_date: str
    min_52_week_price: str
    max_52_week_price: str
    avg_trading_volume_2m: str
    market_value: str
    enterprise_value: str
    last_balance_sheet_date: str
    total_shares: str
    daily_variation_pct: str
    monthly_variation_pct: str
    variation_30d_pct: str
    variation_12m_pct: str
    current_year_variation_pct: str
    year_minus_1_variation_pct: str
    year_minus_2_variation_pct: str
    year_minus_3_variation_pct: str
    year_minus_4_variation_pct: str
    year_minus_5_variation_pct: str
    price_to_earnings_ratio: str
    price_to_book_ratio: str
    price_to_ebit_ratio: str
    price_to_sales_ratio: str
    price_to_assets_ratio: str
    price_to_working_capital_ratio: str
    price_to_net_current_assets_ratio: str
    dividend_yield: str
    ev_to_ebitda_ratio: str
    ev_to_ebit_ratio: str
    net_revenue_5y_growth_pct: str
    earnings_per_share: str
    book_value_per_share: str
    gross_margin_pct: str
    ebit_margin_pct: str
    net_margin_pct: str
    ebit_to_assets_ratio: str
    return_on_invested_capital: str
    return_on_equity: str
    current_liquidity_ratio: str
    gross_debt_to_equity_ratio: str
    asset_turnover_ratio: str
    total_assets: str
    cash_and_equivalents: str
    current_assets: str
    gross_debt: str
    net_debt: str
    shareholders_equity: str
    net_revenue_12m: str
    ebit_12m: str
    net_income_12m: str
    net_revenue_3m: str
    ebit_3m: str
    net_income_3m: str
    execution_datetime: str
    execution_date: int

    def __post_init__(self):
        """
        Post-initialization method to normalize data.
        """
        # Normalize required string fields
        self.stock_ticker = self.stock_ticker.strip().upper()
        self.stock_type = self.stock_type.strip().upper()
        self.company_name = self.company_name.strip().upper()
        self.sector_name = self.sector_name.strip().upper()
        self.subsector_name = self.subsector_name.strip().upper()

        # Validate required fields
        if not self.stock_ticker:
            raise ValueError("stock_ticker cannot be empty")
        if not self.company_name:
            raise ValueError("company_name cannot be empty")
