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
        nome_papel (str): Stock ticker symbol on B3
        tipo_papel (str): Stock type (ON = common, PN = preferred, etc.)
        nome_empresa (str): Company's commercial name
        nome_setor (str): Company's sector classification
        nome_subsetor (str): Company's subsector classification
        vlr_cot (Optional[float]): Current stock price
        dt_ult_cot (str): Date of last trading session
        vlr_cot_min_52_sem (Optional[float]): 52-week low price
        vlr_cot_max_52_sem (Optional[float]): 52-week high price
        vol_med_neg_2m (Optional[float]): Average trading volume in last 2 months
        vlr_mercado (Optional[float]): Market value of the company
        vlr_firma (Optional[float]): Enterprise value (market value + net debt)
        dt_ult_balanco_proc (str): Date of last processed balance sheet
        num_acoes (Optional[float]): Total number of shares
        pct_var_dia (Optional[float]): Daily price variation percentage
        pct_var_mes (Optional[float]): Monthly price variation percentage
        pct_var_30d (Optional[float]): 30-day price variation percentage
        pct_var_12m (Optional[float]): 12-month price variation percentage
        pct_var_ano_a0 (Optional[float]): Current year price variation percentage
        pct_var_ano_a1 (Optional[float]): Previous year price variation percentage
        pct_var_ano_a2 (Optional[float]): Two years ago price variation percentage
        pct_var_ano_a3 (Optional[float]): Three years ago price variation percentage
        pct_var_ano_a4 (Optional[float]): Four years ago price variation percentage
        pct_var_ano_a5 (Optional[float]): Five years ago price variation percentage
        vlr_p_sobre_l (Optional[float]): Price-to-Earnings ratio (P/E)
        vlr_p_sobre_vp (Optional[float]): Price-to-Book ratio (P/B)
        vlr_p_sobre_ebit (Optional[float]): Price-to-EBIT ratio
        vlr_psr (Optional[float]): Price-to-Sales ratio (PSR)
        vlr_p_sobre_ativ (Optional[float]): Price-to-Assets ratio
        vlr_p_sobre_cap_giro (Optional[float]): Price-to-Working Capital ratio
        vlr_p_sobre_ativ_circ_liq (Optional[float]): Price-to-Net Current Assets ratio
        vlr_div_yield (Optional[float]): Dividend yield percentage
        vlr_ev_sobre_ebitda (Optional[float]): Enterprise Value to EBITDA ratio
        vlr_ev_sobre_ebit (Optional[float]): Enterprise Value to EBIT ratio
        pct_cresc_rec_liq_ult_5a (Optional[float]): 5-year net revenue growth percentage
        vlr_lpa (Optional[float]): Earnings per share (EPS)
        vlr_vpa (Optional[float]): Book value per share
        vlr_margem_bruta (Optional[float]): Gross margin percentage
        vlr_margem_ebit (Optional[float]): EBIT margin percentage
        vlr_margem_liq (Optional[float]): Net margin percentage
        vlr_ebit_sobre_ativo (Optional[float]): EBIT over assets ratio
        vlr_roic (Optional[float]): Return on invested capital (ROIC)
        vlr_roe (Optional[float]): Return on equity (ROE)
        vlr_liquidez_corr (Optional[float]): Current liquidity ratio
        vlr_divida_bruta_sobre_patrim (Optional[float]): Gross debt to equity ratio
        vlr_giro_ativos (Optional[float]): Asset turnover ratio
        vlr_ativo (Optional[float]): Total assets value
        vlr_disponibilidades (Optional[float]): Cash and cash equivalents
        vlr_ativ_circulante (Optional[float]): Current assets value
        vlr_divida_bruta (Optional[float]): Gross debt value
        vlr_divida_liq (Optional[float]): Net debt value
        vlr_patrim_liq (Optional[float]): Shareholders' equity value
        vlr_receita_liq_ult_12m (Optional[float]): Net revenue in last 12 months
        vlr_ebit_ult_12m (Optional[float]): EBIT in last 12 months
        vlr_lucro_liq_ult_12m (Optional[float]): Net income in last 12 months
        vlr_receita_liq_ult_3m (Optional[float]): Net revenue in last 3 months
        vlr_ebit_ult_3m (Optional[float]): EBIT in last 3 months
        vlr_lucro_liq_ult_3m (Optional[float]): Net income in last 3 months
        execution_date (str): Date reference for data extraction
    """

    nome_papel: str
    tipo_papel: str
    nome_empresa: str
    nome_setor: str
    nome_subsetor: str
    vlr_cot: Optional[float]
    dt_ult_cot: str
    vlr_cot_min_52_sem: Optional[float]
    vlr_cot_max_52_sem: Optional[float]
    vol_med_neg_2m: Optional[float]
    vlr_mercado: Optional[float]
    vlr_firma: Optional[float]
    dt_ult_balanco_proc: str
    num_acoes: Optional[float]
    pct_var_dia: Optional[float]
    pct_var_mes: Optional[float]
    pct_var_30d: Optional[float]
    pct_var_12m: Optional[float]
    pct_var_ano_a0: Optional[float]
    pct_var_ano_a1: Optional[float]
    pct_var_ano_a2: Optional[float]
    pct_var_ano_a3: Optional[float]
    pct_var_ano_a4: Optional[float]
    pct_var_ano_a5: Optional[float]
    vlr_p_sobre_l: Optional[float]
    vlr_p_sobre_vp: Optional[float]
    vlr_p_sobre_ebit: Optional[float]
    vlr_psr: Optional[float]
    vlr_p_sobre_ativ: Optional[float]
    vlr_p_sobre_cap_giro: Optional[float]
    vlr_p_sobre_ativ_circ_liq: Optional[float]
    vlr_div_yield: Optional[float]
    vlr_ev_sobre_ebitda: Optional[float]
    vlr_ev_sobre_ebit: Optional[float]
    pct_cresc_rec_liq_ult_5a: Optional[float]
    vlr_lpa: Optional[float]
    vlr_vpa: Optional[float]
    vlr_margem_bruta: Optional[float]
    vlr_margem_ebit: Optional[float]
    vlr_margem_liq: Optional[float]
    vlr_ebit_sobre_ativo: Optional[float]
    vlr_roic: Optional[float]
    vlr_roe: Optional[float]
    vlr_liquidez_corr: Optional[float]
    vlr_divida_bruta_sobre_patrim: Optional[float]
    vlr_giro_ativos: Optional[float]
    vlr_ativo: Optional[float]
    vlr_disponibilidades: Optional[float]
    vlr_ativ_circulante: Optional[float]
    vlr_divida_bruta: Optional[float]
    vlr_divida_liq: Optional[float]
    vlr_patrim_liq: Optional[float]
    vlr_receita_liq_ult_12m: Optional[float]
    vlr_ebit_ult_12m: Optional[float]
    vlr_lucro_liq_ult_12m: Optional[float]
    vlr_receita_liq_ult_3m: Optional[float]
    vlr_ebit_ult_3m: Optional[float]
    vlr_lucro_liq_ult_3m: Optional[float]
    execution_date: str

    def __post_init__(self):
        # Normalize required string fields
        self.nome_papel = self.nome_papel.strip().upper()
        self.tipo_papel = self.tipo_papel.strip().upper()
        self.nome_empresa = self.nome_empresa.strip().upper()
        self.nome_setor = self.nome_setor.strip().upper()
        self.nome_subsetor = self.nome_subsetor.strip().upper()

        # Validate required fields
        if not self.nome_papel:
            raise ValueError("nome_papel cannot be empty")
        if not self.nome_empresa:
            raise ValueError("nome_empresa cannot be empty")
