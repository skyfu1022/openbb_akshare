"""AKShare Index Constituents Model."""

# pylint: disable=unused-argument

import re
from typing import Any, Dict, List, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.index_constituents import (
    IndexConstituentsData,
    IndexConstituentsQueryParams,
)


class AKShareIndexConstituentsQueryParams(IndexConstituentsQueryParams):
    """AKShare Index Constituents Query.

    Source: https://akshare.akfamily.xyz/data/index/index.html
    """


class AKShareIndexConstituentsData(IndexConstituentsData):
    """AKShare Index Constituents Data."""

    __alias_dict__ = {
        "symbol": "成分券代码",
        "name": "成分券名称",
    }


class AKShareIndexConstituentsFetcher(
    Fetcher[
        AKShareIndexConstituentsQueryParams,
        List[AKShareIndexConstituentsData],
    ]
):
    """Transform the query, extract and transform the data from the AKShare endpoints."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> AKShareIndexConstituentsQueryParams:
        """Transform the query params."""
        return AKShareIndexConstituentsQueryParams(**params)

    @staticmethod
    def extract_data(
        query: AKShareIndexConstituentsQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the AKShare endpoint."""
        import akshare as ak

        symbol = re.sub(r"^(SH|SZ|BJ)", "", query.symbol)
        df = ak.index_stock_cons_csindex(symbol=symbol)
        df = df[["成分券代码", "成分券名称"]]

        return df.to_dict(orient="records")

    @staticmethod
    def transform_data(
        query: AKShareIndexConstituentsQueryParams, data: List[Dict], **kwargs: Any
    ) -> List[AKShareIndexConstituentsData]:
        """Return the transformed data."""
        return [AKShareIndexConstituentsData.model_validate(d) for d in data]
