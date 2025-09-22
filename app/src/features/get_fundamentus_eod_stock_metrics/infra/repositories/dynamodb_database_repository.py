import os
from datetime import datetime, UTC

import boto3
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute

from app.src.features.get_fundamentus_eod_stock_metrics.domain.interfaces.database_repository_interface import (
    IDatabaseRepository
)
from app.src.features.get_fundamentus_eod_stock_metrics.domain.entities.fundamentus_stock_metrics import (
    FundamentusStockMetrics
)

from app.src.features.cross.utils.log import LogUtils
from app.src.features.cross.utils.serialization import SerializationUtils
from app.src.features.cross.utils.decorators import timing_decorator


class FundamentusStockMetricsModel(Model):
    """
    PynamoDB model for Fundamentus stock metrics data.
    """
    class Meta:
        table_name = os.getenv("DYNAMODB_FUNDAMENTUS_EOD_STOCK_METRICS_TABLE_NAME")
        region = boto3.session.Session().region_name

    # Primary key: stock ticker symbol
    nome_papel = UnicodeAttribute(hash_key=True)
    
    # Sort key: execution date for versioning
    execution_date = UnicodeAttribute(range_key=True)

    # Execution timestamp for record creation
    execution_timestamp = UnicodeAttribute()
    
    # Basic stock information (nullable)
    tipo_papel = UnicodeAttribute(null=True)
    nome_empresa = UnicodeAttribute(null=True)
    nome_setor = UnicodeAttribute(null=True)
    nome_subsetor = UnicodeAttribute(null=True)

    # Price and trading information (nullable)
    vlr_cot = NumberAttribute(null=True)
    dt_ult_cot = UnicodeAttribute(null=True)
    vlr_cot_min_52_sem = NumberAttribute(null=True)
    vlr_cot_max_52_sem = NumberAttribute(null=True)
    vol_med_neg_2m = NumberAttribute(null=True)
    
    # Market and financial values (nullable)
    vlr_mercado = NumberAttribute(null=True)
    vlr_firma = NumberAttribute(null=True)
    dt_ult_balanco_proc = UnicodeAttribute(null=True)
    num_acoes = NumberAttribute(null=True)
    
    # Price variation percentages (nullable)
    pct_var_dia = NumberAttribute(null=True)
    pct_var_mes = NumberAttribute(null=True)
    pct_var_30d = NumberAttribute(null=True)
    pct_var_12m = NumberAttribute(null=True)
    pct_var_ano_a0 = NumberAttribute(null=True)
    pct_var_ano_a1 = NumberAttribute(null=True)
    pct_var_ano_a2 = NumberAttribute(null=True)
    pct_var_ano_a3 = NumberAttribute(null=True)
    pct_var_ano_a4 = NumberAttribute(null=True)
    pct_var_ano_a5 = NumberAttribute(null=True)
    
    # Valuation ratios (nullable)
    vlr_p_sobre_l = NumberAttribute(null=True)
    vlr_p_sobre_vp = NumberAttribute(null=True)
    vlr_p_sobre_ebit = NumberAttribute(null=True)
    vlr_psr = NumberAttribute(null=True)
    vlr_p_sobre_ativ = NumberAttribute(null=True)
    vlr_p_sobre_cap_giro = NumberAttribute(null=True)
    vlr_p_sobre_ativ_circ_liq = NumberAttribute(null=True)
    vlr_div_yield = NumberAttribute(null=True)
    vlr_ev_sobre_ebitda = NumberAttribute(null=True)
    vlr_ev_sobre_ebit = NumberAttribute(null=True)
    pct_cresc_rec_liq_ult_5a = NumberAttribute(null=True)
    
    # Per-share metrics (nullable)
    vlr_lpa = NumberAttribute(null=True)
    vlr_vpa = NumberAttribute(null=True)
    
    # Profitability ratios (nullable)
    vlr_margem_bruta = NumberAttribute(null=True)
    vlr_margem_ebit = NumberAttribute(null=True)
    vlr_margem_liq = NumberAttribute(null=True)
    vlr_ebit_sobre_ativo = NumberAttribute(null=True)
    vlr_roic = NumberAttribute(null=True)
    vlr_roe = NumberAttribute(null=True)
    
    # Liquidity and debt ratios (nullable)
    vlr_liquidez_corr = NumberAttribute(null=True)
    vlr_divida_bruta_sobre_patrim = NumberAttribute(null=True)
    vlr_giro_ativos = NumberAttribute(null=True)
    
    # Balance sheet items (nullable)
    vlr_ativo = NumberAttribute(null=True)
    vlr_disponibilidades = NumberAttribute(null=True)
    vlr_ativ_circulante = NumberAttribute(null=True)
    vlr_divida_bruta = NumberAttribute(null=True)
    vlr_divida_liq = NumberAttribute(null=True)
    vlr_patrim_liq = NumberAttribute(null=True)
    
    # Income statement items (12 months) (nullable)
    vlr_receita_liq_ult_12m = NumberAttribute(null=True)
    vlr_ebit_ult_12m = NumberAttribute(null=True)
    vlr_lucro_liq_ult_12m = NumberAttribute(null=True)
    
    # Income statement items (3 months) (nullable)
    vlr_receita_liq_ult_3m = NumberAttribute(null=True)
    vlr_ebit_ult_3m = NumberAttribute(null=True)
    vlr_lucro_liq_ult_3m = NumberAttribute(null=True)

    def __init__(self, *args, **kwargs):
        self.Meta.table_name = os.getenv("DYNAMODB_FUNDAMENTUS_EOD_STOCK_METRICS_TABLE_NAME")
        super().__init__(*args, **kwargs)


class DynamoDBDatabaseRepository(IDatabaseRepository):
    """
    Implementation of the Fundamentus stock metrics repository using DynamoDB.
    """
    def __init__(self):
        self.logger = LogUtils.setup_logger(name=__name__)


    @timing_decorator
    def batch_save_stock_metrics(self, items: list[FundamentusStockMetrics]) -> None:
        """
        Saves a batch of stock metrics data to the repository.

        Args:
            items (list[FundamentusStockMetrics]): List of stock metrics to save.
        """
        try:
            with FundamentusStockMetricsModel.batch_write() as batch:
                for _, item in enumerate(items):
                    model = FundamentusStockMetricsModel(**SerializationUtils.json_serialize(item))
                    batch.save(model)
                    
            self.logger.info(f"Successfully batch saved {len(items)} stock metrics "
                             f"to table {FundamentusStockMetricsModel.Meta.table_name}")

        except Exception:
            self.logger.exception(f"Error batch saving stock metrics to table "
                                 f"{FundamentusStockMetricsModel.Meta.table_name}")
            raise
