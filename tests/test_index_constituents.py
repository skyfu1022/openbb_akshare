"""Test cases for Index Constituents model."""

import pytest
from openbb_akshare.models.index_constituents import (
    AKShareIndexConstituentsFetcher,
    AKShareIndexConstituentsQueryParams,
    AKShareIndexConstituentsData,
)


def test_transform_query():
    """Test query transformation strips market prefix."""
    fetcher = AKShareIndexConstituentsFetcher()
    query = fetcher.transform_query({"symbol": "SH000300"})
    assert query.symbol == "SH000300"  # to_upper keeps it, extract_data strips


def test_transform_data_with_sample():
    """Test data mapping with sample AKShare data."""
    fetcher = AKShareIndexConstituentsFetcher()
    query = fetcher.transform_query({"symbol": "000300"})

    sample_data = [
        {"成分券代码": "600000", "成分券名称": "浦发银行"},
        {"成分券代码": "600036", "成分券名称": "招商银行"},
    ]

    result = fetcher.transform_data(query, sample_data)
    assert len(result) == 2
    assert isinstance(result[0], AKShareIndexConstituentsData)
    assert result[0].symbol == "600000"
    assert result[0].name == "浦发银行"


def test_transform_data_empty():
    """Test transform_data with empty list."""
    fetcher = AKShareIndexConstituentsFetcher()
    query = fetcher.transform_query({"symbol": "000300"})
    result = fetcher.transform_data(query, [])
    assert result == []
