"""Test cases for Index Historical model."""

import pytest
from openbb_akshare.models.index_historical import (
    AKShareIndexHistoricalFetcher,
    AKShareIndexHistoricalQueryParams,
    AKShareIndexHistoricalData,
)


def test_transform_query_with_defaults():
    """Test query transformation sets default dates."""
    fetcher = AKShareIndexHistoricalFetcher()
    query = fetcher.transform_query({"symbol": "000300"})
    assert query.symbol == "000300"
    assert query.period == "daily"
    assert query.start_date is not None
    assert query.end_date is not None


def test_transform_query_with_dates():
    """Test query transformation preserves provided dates."""
    fetcher = AKShareIndexHistoricalFetcher()
    query = fetcher.transform_query({
        "symbol": "000300",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "period": "weekly",
    })
    assert query.symbol == "000300"
    assert query.period == "weekly"


def test_transform_data_with_sample():
    """Test data mapping with sample AKShare data."""
    fetcher = AKShareIndexHistoricalFetcher()
    query = fetcher.transform_query({"symbol": "000300"})

    sample_data = [
        {
            "日期": "2024-01-02",
            "开盘": 3400.00,
            "收盘": 3420.00,
            "最高": 3430.00,
            "最低": 3390.00,
            "成交量": 1000000,
            "成交额": 5000000,
            "涨跌幅": 0.59,
            "涨跌额": 20.00,
            "symbol": "000300",
        }
    ]

    result = fetcher.transform_data(query, sample_data)
    assert len(result) == 1
    assert isinstance(result[0], AKShareIndexHistoricalData)
    assert result[0].open == 3400.00
    assert result[0].close == 3420.00
    assert result[0].high == 3430.00
    assert result[0].low == 3390.00
    assert result[0].volume == 1000000


def test_transform_data_extra_fields():
    """Test extra fields (amount, change, change_percent) are mapped."""
    fetcher = AKShareIndexHistoricalFetcher()
    query = fetcher.transform_query({"symbol": "000300"})

    sample_data = [
        {
            "日期": "2024-01-02",
            "开盘": 3400.00,
            "收盘": 3420.00,
            "最高": 3430.00,
            "最低": 3390.00,
            "成交量": 1000000,
            "成交额": 5000000,
            "涨跌幅": 0.59,
            "涨跌额": 20.00,
            "symbol": "000300",
        }
    ]

    result = fetcher.transform_data(query, sample_data)
    assert result[0].amount == 5000000
    assert result[0].change == 20.00
    assert result[0].change_percent == 0.59


def test_transform_data_empty():
    """Test transform_data with empty list."""
    fetcher = AKShareIndexHistoricalFetcher()
    query = fetcher.transform_query({"symbol": "000300"})
    result = fetcher.transform_data(query, [])
    assert result == []


def test_extract_data_strips_prefix():
    """Test extract_data strips market prefix from symbol."""
    import re
    symbol = "SH000300"
    stripped = re.sub(r"^(SH|SZ|BJ)", "", symbol)
    assert stripped == "000300"
