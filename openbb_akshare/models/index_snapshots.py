"""AKShare Index Snapshots Model."""

# pylint: disable=unused-argument

from typing import Any, Dict, List, Literal, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.index_snapshots import (
    IndexSnapshotsData,
    IndexSnapshotsQueryParams,
)
from pydantic import Field


class AKShareIndexSnapshotsQueryParams(IndexSnapshotsQueryParams):
    """AKShare Index Snapshots Query.

    Source: https://akshare.akfamily.xyz/data/index/index.html
    """

    __json_schema_extra__ = {
        "category": {
            "choices": [
                "沪深重要指数",
                "上证系列指数",
                "深证系列指数",
                "指数成份",
                "中证系列指数",
            ]
        },
    }

    region: str = Field(
        default="cn",
        description="The region of focus for the data.",
    )

    category: Literal[
        "沪深重要指数",
        "上证系列指数",
        "深证系列指数",
        "指数成份",
        "中证系列指数",
    ] = Field(
        default="沪深重要指数",
        description="Index category for AKShare API.",
    )


class AKShareIndexSnapshotsData(IndexSnapshotsData):
    """AKShare Index Snapshots Data."""

    __alias_dict__ = {
        "symbol": "代码",
        "name": "名称",
        "price": "最新价",
        "open": "今开",
        "high": "最高",
        "low": "最低",
        "prev_close": "昨收",
        "volume": "成交量",
        "change": "涨跌额",
        "change_percent": "涨跌幅",
    }

    change: Optional[float] = Field(
        default=None, description="Change in value of the index."
    )
    change_percent: Optional[float] = Field(
        default=None,
        description="Change, in normalized percentage points, of the index.",
    )


class AKShareIndexSnapshotsFetcher(
    Fetcher[
        AKShareIndexSnapshotsQueryParams,
        List[AKShareIndexSnapshotsData],
    ]
):
    """Transform the query, extract and transform the data from the AKShare endpoints."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> AKShareIndexSnapshotsQueryParams:
        """Transform the query params."""
        return AKShareIndexSnapshotsQueryParams(**params)

    @staticmethod
    def extract_data(
        query: AKShareIndexSnapshotsQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the AKShare endpoint."""
        import akshare as ak

        df = ak.stock_zh_index_spot_em(symbol=query.category)
        df["currency"] = "CNY"

        return df.to_dict(orient="records")

    @staticmethod
    def transform_data(
        query: AKShareIndexSnapshotsQueryParams, data: List[Dict], **kwargs: Any
    ) -> List[AKShareIndexSnapshotsData]:
        """Return the transformed data."""
        return [AKShareIndexSnapshotsData.model_validate(d) for d in data]
