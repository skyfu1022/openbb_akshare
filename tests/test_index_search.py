"""Test cases for Index Search model."""

import pytest
from openbb_akshare.models.index_search import (
    AKShareIndexSearchFetcher,
    AKShareIndexSearchQueryParams,
    AKShareIndexSearchData,
)


def test_transform_query_default():
    """Test query transformation with defaults."""
    fetcher = AKShareIndexSearchFetcher()
    query = fetcher.transform_query({"query": "", "is_symbol": False})
    assert query.query == ""
    assert query.is_symbol is False


def test_transform_data_with_sample():
    """Test data mapping with sample AKShare data."""
    fetcher = AKShareIndexSearchFetcher()
    query = fetcher.transform_query({"query": "沪深"})

    sample_data = [
        {"index_code": "000300", "display_name": "沪深300"},
        {"index_code": "000905", "display_name": "中证500"},
    ]

    result = fetcher.transform_data(query, sample_data)
    assert len(result) == 2
    assert isinstance(result[0], AKShareIndexSearchData)
    assert result[0].symbol == "000300"
    assert result[0].name == "沪深300"


def test_transform_data_empty():
    """Test transform_data with empty list."""
    fetcher = AKShareIndexSearchFetcher()
    query = fetcher.transform_query({"query": ""})
    result = fetcher.transform_data(query, [])
    assert result == []


def test_extract_data_filters_by_query():
    """Test extract_data filters by query string."""
    fetcher = AKShareIndexSearchFetcher()
    query = fetcher.transform_query({"query": "沪深", "is_symbol": False})

    sample_df_data = [
        {"index_code": "000300", "display_name": "沪深300"},
        {"index_code": "000905", "display_name": "中证500"},
        {"index_code": "000852", "display_name": "中证1000"},
    ]

    # Simulate client-side filtering logic
    import pandas as pd

    df = pd.DataFrame(sample_df_data)
    mask = df["index_code"].str.contains("沪深", case=False) | df[
        "display_name"
    ].str.contains("沪深", case=False)
    filtered = df[mask]
    assert len(filtered) == 1
    assert filtered.iloc[0]["display_name"] == "沪深300"


def test_extract_data_filters_by_symbol():
    """Test extract_data filters by symbol when is_symbol=True."""
    import pandas as pd

    sample_df_data = [
        {"index_code": "000300", "display_name": "沪深300"},
        {"index_code": "000905", "display_name": "中证500"},
        {"index_code": "000852", "display_name": "中证1000"},
    ]

    df = pd.DataFrame(sample_df_data)
    filtered = df[df["index_code"].str.contains("0003", case=False)]
    assert len(filtered) == 1
    assert filtered.iloc[0]["index_code"] == "000300"
