"""AKShare Index Historical Model."""

# pylint: disable=unused-argument

import re
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from dateutil.relativedelta import relativedelta
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.index_historical import (
    IndexHistoricalData,
    IndexHistoricalQueryParams,
)
from openbb_core.provider.utils.descriptions import QUERY_DESCRIPTIONS
from openbb_core.provider.utils.errors import EmptyDataError
from pydantic import Field


class AKShareIndexHistoricalQueryParams(IndexHistoricalQueryParams):
    """AKShare Index Historical Query.

    Source: https://akshare.akfamily.xyz/data/index/index.html
    """

    __json_schema_extra__ = {
        "period": {"choices": ["daily", "weekly", "monthly"]},
    }

    period: Literal["daily", "weekly", "monthly"] = Field(
        default="daily",
        description=QUERY_DESCRIPTIONS.get("period", ""),
    )


class AKShareIndexHistoricalData(IndexHistoricalData):
    """AKShare Index Historical Data."""

    __alias_dict__ = {
        "date": "日期",
        "open": "开盘",
        "close": "收盘",
        "high": "最高",
        "low": "最低",
        "volume": "成交量",
        "amount": "成交额",
        "change": "涨跌额",
        "change_percent": "涨跌幅",
    }

    amount: Optional[float] = Field(
        default=None,
        description="Trading amount.",
    )
    change: Optional[float] = Field(
        default=None,
        description="Change in the price from the previous close.",
    )
    change_percent: Optional[float] = Field(
        default=None,
        description="Change in the price from the previous close, as a normalized percent.",
    )


class AKShareIndexHistoricalFetcher(
    Fetcher[
        AKShareIndexHistoricalQueryParams,
        List[AKShareIndexHistoricalData],
    ]
):
    """Transform the query, extract and transform the data from the AKShare endpoints."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> AKShareIndexHistoricalQueryParams:
        """Transform the query params."""
        transformed_params = params.copy()

        now = datetime.now().date()
        if params.get("start_date") is None:
            transformed_params["start_date"] = now - relativedelta(years=1)
        if params.get("end_date") is None:
            transformed_params["end_date"] = now

        return AKShareIndexHistoricalQueryParams(**transformed_params)

    @staticmethod
    def extract_data(
        query: AKShareIndexHistoricalQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the AKShare endpoint."""
        import akshare as ak

        symbol = re.sub(r"^(SH|SZ|BJ)", "", query.symbol)
        start_date = (
            query.start_date.strftime("%Y%m%d") if query.start_date else "19700101"
        )
        end_date = (
            query.end_date.strftime("%Y%m%d") if query.end_date else "22220101"
        )

        df = ak.index_zh_a_hist(
            symbol=symbol,
            period=query.period,
            start_date=start_date,
            end_date=end_date,
        )

        if df.empty:
            raise EmptyDataError()

        df = df.drop(columns=["振幅", "换手率"], errors="ignore")
        df["symbol"] = symbol

        return df.to_dict(orient="records")

    @staticmethod
    def transform_data(
        query: AKShareIndexHistoricalQueryParams, data: List[Dict], **kwargs: Any
    ) -> List[AKShareIndexHistoricalData]:
        """Return the transformed data."""
        return [AKShareIndexHistoricalData.model_validate(d) for d in data]
