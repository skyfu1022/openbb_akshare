"""Test cases for Index Snapshots model."""

import pytest
from openbb_akshare.models.index_snapshots import (
    AKShareIndexSnapshotsFetcher,
    AKShareIndexSnapshotsQueryParams,
    AKShareIndexSnapshotsData,
)


def test_transform_query_default():
    """Test query transformation with defaults."""
    fetcher = AKShareIndexSnapshotsFetcher()
    query = fetcher.transform_query({})
    assert query.region == "cn"
    assert query.category == "沪深重要指数"


def test_transform_query_custom_category():
    """Test query with custom category."""
    fetcher = AKShareIndexSnapshotsFetcher()
    query = fetcher.transform_query({"category": "上证系列指数"})
    assert query.category == "上证系列指数"


def test_transform_data_with_sample():
    """Test data mapping with sample AKShare data."""
    fetcher = AKShareIndexSnapshotsFetcher()
    query = fetcher.transform_query({})

    sample_data = [
        {
            "代码": "000001",
            "名称": "上证指数",
            "最新价": 3000.00,
            "涨跌额": 10.00,
            "涨跌幅": 0.33,
            "昨收": 2990.00,
            "今开": 2995.00,
            "最高": 3010.00,
            "最低": 2980.00,
            "成交量": 1000000,
            "成交额": 5000000,
            "currency": "CNY",
        }
    ]

    result = fetcher.transform_data(query, sample_data)
    assert len(result) == 1
    assert isinstance(result[0], AKShareIndexSnapshotsData)
    assert result[0].symbol == "000001"
    assert result[0].name == "上证指数"
    assert result[0].price == 3000.00
    assert result[0].open == 2995.00
    assert result[0].high == 3010.00
    assert result[0].low == 2980.00
    assert result[0].prev_close == 2990.00
    assert result[0].volume == 1000000
    assert result[0].change == 10.00
    assert result[0].change_percent == 0.33
    assert result[0].currency == "CNY"


def test_transform_data_close_is_none():
    """Test that close field is None in snapshot data (no closing price in real-time)."""
    fetcher = AKShareIndexSnapshotsFetcher()
    query = fetcher.transform_query({})

    sample_data = [
        {
            "代码": "000001",
            "名称": "上证指数",
            "最新价": 3000.00,
            "涨跌额": 10.00,
            "涨跌幅": 0.33,
            "昨收": 2990.00,
            "今开": 2995.00,
            "最高": 3010.00,
            "最低": 2980.00,
            "成交量": 1000000,
            "成交额": 5000000,
            "currency": "CNY",
        }
    ]

    result = fetcher.transform_data(query, sample_data)
    assert result[0].close is None


def test_transform_data_empty():
    """Test transform_data with empty list."""
    fetcher = AKShareIndexSnapshotsFetcher()
    query = fetcher.transform_query({})
    result = fetcher.transform_data(query, [])
    assert result == []
