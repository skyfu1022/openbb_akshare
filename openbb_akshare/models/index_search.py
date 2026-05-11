"""AKShare Index Search Model."""

# pylint: disable=unused-argument

from typing import Any, Dict, List, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.index_search import (
    IndexSearchData,
    IndexSearchQueryParams,
)


class AKShareIndexSearchQueryParams(IndexSearchQueryParams):
    """AKShare Index Search Query.

    Source: https://akshare.akfamily.xyz/data/index/index.html
    """


class AKShareIndexSearchData(IndexSearchData):
    """AKShare Index Search Data."""

    __alias_dict__ = {
        "symbol": "index_code",
        "name": "display_name",
    }


class AKShareIndexSearchFetcher(
    Fetcher[
        AKShareIndexSearchQueryParams,
        List[AKShareIndexSearchData],
    ]
):
    """Transform the query, extract and transform the data from the AKShare endpoints."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> AKShareIndexSearchQueryParams:
        """Transform the query params."""
        return AKShareIndexSearchQueryParams(**params)

    @staticmethod
    def extract_data(
        query: AKShareIndexSearchQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the AKShare endpoint."""
        import akshare as ak

        df = ak.index_stock_info()

        if query.query:
            if query.is_symbol:
                df = df[df["index_code"].str.contains(query.query, case=False)]
            else:
                mask = df["index_code"].str.contains(query.query, case=False) | df[
                    "display_name"
                ].str.contains(query.query, case=False)
                df = df[mask]

        return df.to_dict(orient="records")

    @staticmethod
    def transform_data(
        query: AKShareIndexSearchQueryParams, data: List[Dict], **kwargs: Any
    ) -> List[AKShareIndexSearchData]:
        """Return the transformed data."""
        return [AKShareIndexSearchData.model_validate(d) for d in data]
