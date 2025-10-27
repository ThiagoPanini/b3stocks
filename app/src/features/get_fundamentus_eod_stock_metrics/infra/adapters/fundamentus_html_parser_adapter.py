from datetime import datetime

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from app.src.features.cross.domain.entities.http_client_request_config import HTTPClientRequestConfig
from app.src.features.get_fundamentus_eod_stock_metrics.domain.interfaces.html_parser_adapter_interface import (
    IHTMLParserAdapter
)
from app.src.features.get_fundamentus_eod_stock_metrics.domain.entities.fundamentus_stock_metrics import (
    FundamentusStockMetrics
)
from app.src.features.cross.utils.decorators import timing_decorator
from app.src.features.cross.utils.log import LogUtils
from app.src.features.cross.domain.value_objects import DateFormat


pd.set_option('future.no_silent_downcasting', True)

# Defining some constants used in the parsing process
VARIATION_HEADINGS = [
    "Dia", "Mês", "30 dias", "12 meses"
] + [str(datetime.now().year - i) for i in range(6)]


STOCK_METRICS_MAPPING = {
    "Papel": "nome_papel",
    "Tipo": "tipo_papel",
    "Empresa": "nome_empresa",
    "Setor": "nome_setor",
    "Subsetor": "nome_subsetor",
    "Cotação": "vlr_cot",
    "Data últ cot": "dt_ult_cot",
    "Min 52 sem": "vlr_cot_min_52_sem",
    "Max 52 sem": "vlr_cot_max_52_sem",
    "Vol $ méd (2m)": "vol_med_neg_2m",
    "Valor de mercado": "vlr_mercado",
    "Valor da firma": "vlr_firma",
    "Últ balanço processado": "dt_ult_balanco_proc",
    "Nro. Ações": "num_acoes",
    "Dia": "pct_var_dia",
    "Mês": "pct_var_mes",
    "30 dias": "pct_var_30d",
    "12 meses": "pct_var_12m",
    str(datetime.now().year): "pct_var_ano_a0",
    str(datetime.now().year - 1): "pct_var_ano_a1",
    str(datetime.now().year - 2): "pct_var_ano_a2",
    str(datetime.now().year - 3): "pct_var_ano_a3",
    str(datetime.now().year - 4): "pct_var_ano_a4",
    str(datetime.now().year - 5): "pct_var_ano_a5",
    "P/L": "vlr_p_sobre_l",
    "P/VP": "vlr_p_sobre_vp",
    "P/EBIT": "vlr_p_sobre_ebit",
    "PSR": "vlr_psr",
    "P/Ativos": "vlr_p_sobre_ativ",
    "P/Cap. Giro": "vlr_p_sobre_cap_giro",
    "P/Ativ Circ Liq": "vlr_p_sobre_ativ_circ_liq",
    "Div. Yield": "vlr_div_yield",
    "EV / EBITDA": "vlr_ev_sobre_ebitda",
    "EV / EBIT": "vlr_ev_sobre_ebit",
    "Cres. Rec (5a)": "pct_cresc_rec_liq_ult_5a",
    "LPA": "vlr_lpa",
    "VPA": "vlr_vpa",
    "Marg. Bruta": "vlr_margem_bruta",
    "Marg. EBIT": "vlr_margem_ebit",
    "Marg. Líquida": "vlr_margem_liq",
    "EBIT / Ativo": "vlr_ebit_sobre_ativo",
    "ROIC": "vlr_roic",
    "ROE": "vlr_roe",
    "Liquidez Corr": "vlr_liquidez_corr",
    "Div Br/ Patrim": "vlr_divida_bruta_sobre_patrim",
    "Giro Ativos": "vlr_giro_ativos",
    "Ativo": "vlr_ativo",
    "Disponibilidades": "vlr_disponibilidades",
    "Ativo Circulante": "vlr_ativ_circulante",
    "Dív. Bruta": "vlr_divida_bruta",
    "Dív. Líquida": "vlr_divida_liq",
    "Patrim. Líq": "vlr_patrim_liq",
    "Receita Líquida_1": "vlr_receita_liq_ult_12m",
    "EBIT_1": "vlr_ebit_ult_12m",
    "Lucro Líquido_1": "vlr_lucro_liq_ult_12m",
    "Receita Líquida": "vlr_receita_liq_ult_3m",
    "EBIT": "vlr_ebit_ult_3m",
    "Lucro Líquido": "vlr_lucro_liq_ult_3m"
}


class FundamentusHTMLParserAdapter(IHTMLParserAdapter):
    """
    Implementation of IHTMLParserAdapter that parses stock tickers from Fundamentus website.
    """

    def __init__(self):
        self.logger = LogUtils.setup_logger(name=__name__)
        self.variation_headings = VARIATION_HEADINGS
        self.stock_metrics_mapping = STOCK_METRICS_MAPPING


    def __parse_float_cols(self, df: pd.DataFrame, cols_list: list) -> pd.DataFrame:
        """
        Convert columns in a pandas DataFrame from string to float.

        This method can be executed to convert string attributes present in a pandas DataFrame into
        float attributes (as long as such strings can be converted to floats). This functionality
        is relevant because, in the raw extraction of information by the scrapper process, all
        attributes are originally set in the pandas DataFrame as strings, which can make further
        analysis difficult for users.

        Args:
            df (pd.DataFrame): The information extracted from the Fundamentus investment website
            cols_list (list): The columns to be treated and subsequently converted.

        Returns:
            A pandas DataFrame with the float fields already converted.
        """
        for col in cols_list:
            df[col] = df[col].replace('[^0-9,.-]', '', regex=True)  # Keep negative signs and decimals
            df[col] = df[col].replace("", np.nan).infer_objects(copy=False)
            df[col] = df[col].replace(",", ".", regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')

        return df


    def __parse_percentage_cols(self, df: pd.DataFrame, cols_list: list) -> pd.DataFrame:
        """
        Convert columns in a pandas DataFrame that represent percentages from string to float.

        Sometimes, the columns in a pandas DataFrame that represent percentages are represented as
        strings with a '%' symbol. This method can be executed to convert such string attributes
        into float attributes (as long as such strings can be converted to floats).

        Args:
            df (pd.DataFrame): The information extracted from the Fundamentus investment website
            cols_list (list): The columns to be treated and subsequently converted.

        Returns:
            A pandas DataFrame with the float fields already converted.
        """
        for col in cols_list:
            # Remove percentage symbol and clean up the data
            df[col] = df[col].str.replace("%", "", regex=False)
            df[col] = df[col].replace("", np.nan).infer_objects(copy=False)
            df[col] = df[col].replace(",", ".", regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce') / 100

        return df


    def parse_html_content(
        self,
        html_content: bytes,
        encoding: str,
        request_config: HTTPClientRequestConfig
    ) -> FundamentusStockMetrics:
        """
        Parses stocks metrics data from the raw HTML content of a HTTP response.

        Args:
            html_content (bytes): The raw HTML content of the HTTP response.
            encoding (str): The encoding used to decode the HTML content.
            request_config (HTTPClientRequestConfig): The object containing metadata of the request.

        Returns:
            A list of B3 stocks data extracted and parsed from the request.
        """

        self.logger.debug(f"Decoding HTML content and parsing it using BeautifulSoup")
        try:
            html_text = html_content.decode(encoding)
            html_parsed = BeautifulSoup(html_text, "html.parser")
        except Exception:
            self.logger.exception(f"Error decoding HTML content and parsing it using BeautifulSoup")
            raise

        self.logger.debug(f"Extracting stock metrics data from the parsed HTML content")
        try:
            # Getting the all tables that contains the stock metrics data
            tables = html_parsed.find_all("table", attrs={'class': 'w728'})
            
            # Iterating over all tables
            stock_metrics_data_raw = []
            for table in tables:
                table_row = table.find_all("tr")

                # Iterating over all rows in each table
                for table_data in table_row:
                    cells_list = table_data.find_all("td")

                    # Getting the headings (cells that contains "?" or are in the variation headings list)
                    headings = [
                        cell.text.replace("?", "").strip()
                        for cell in cells_list
                        if "?" in cell.text or cell.text in self.variation_headings
                    ]

                    # Handling duplicated headings by appending a suffix to make them unique
                    for header in headings:
                        if headings.count(header) > 1:
                            new_header_name = header + "_1"
                            headings[headings.index(header)] = new_header_name

                    # Getting all values (cells that are not "?" and not in the headings list)
                    values = [
                        cell.text.strip() for cell in cells_list
                        if ("?" not in cell.text) and (cell.text not in headings)
                    ]

                    # Building a dictionary with headings as keys and values as values
                    table_data_dict = {
                        header: value for header, value in zip(headings, values)
                    }

                    if table_data_dict != {}:
                        stock_metrics_data_raw.append(table_data_dict)
            
            # Building a consolidated dictionary with all stock metrics data
            stock_metrics_data = {
                name: value for dictionary in stock_metrics_data_raw
                for name, value in dictionary.items()
            }

            if not "Papel" in stock_metrics_data:
                raise ValueError(f"Error parsing stock metrics on URL {request_config.url} because "
                                 "'Papel' key couldn't be found on the parsed data")
        
        except Exception:
            self.logger.exception("Error extracting stock metrics from HTML content")
            raise

        self.logger.debug("Initializing a pandas DataFrame to manipulate the stock metrics data")
        try:
            df_stock_metrics = pd.DataFrame(stock_metrics_data, index=[0])
            df_stock_metrics.rename(
                columns=self.stock_metrics_mapping,
                errors="ignore",
                inplace=True
            )

            dataset_cols = list(self.stock_metrics_mapping.values())
            df_stock_metrics = df_stock_metrics[dataset_cols]
        
        except KeyError:
            self.logger.debug(f"Error adapting stock metrics to a DataFrame because some expected "
                              "columns are missing and this is probably due to changes in the HTML "
                              "structure of the Fundamentus website. Columns that are missing will "
                              "be filled with None values.")
            for col in dataset_cols:
                if col not in list(df_stock_metrics.columns):
                    df_stock_metrics[col] = None
        
        # Reordering columns and adding the execution date column
        df_stock_metrics = df_stock_metrics[dataset_cols]
        df_stock_metrics.loc[:, ["execution_date"]] = datetime.now().strftime(DateFormat.DATE.value)

        self.logger.debug("Parsing and converting the numeric data types of the DataFrame columns")
        try:
            float_cols_to_parse = [
                col for col in list(df_stock_metrics.columns)
                if col[:4] in ("vlr_", "vol_", "num_", "pct_", "qtd_", "max_", "min_", "total_")
            ]
            percent_cols_to_parse = [col for col in float_cols_to_parse if col[:4] in ("pct_")]

            # First parse percentage columns (while they're still strings)
            df_stock_metrics_percent_prep = self.__parse_percentage_cols(
                df=df_stock_metrics,
                cols_list=percent_cols_to_parse
            )

            # Then parse remaining float columns (excluding percentage columns)
            non_percent_float_cols = [col for col in float_cols_to_parse if col not in percent_cols_to_parse]
            df_stock_metrics_prep = self.__parse_float_cols(
                df=df_stock_metrics_percent_prep,
                cols_list=non_percent_float_cols
            )
        
        except Exception:
            self.logger.exception("Error parsing and converting the numeric data types of the "
                                  "DataFrame columns")
            raise

        self.logger.debug("Adapting the DataFrame to an instance of FundamentusStockMetrics entity")
        try:
            stock_metrics = FundamentusStockMetrics(**df_stock_metrics_prep.to_dict(orient="records")[0])
        except Exception:
            self.logger.exception("Error adapting the DataFrame to FundamentusStockMetrics entity")
            raise

        return stock_metrics
