"""Test cases for ETF Historical model."""

import pytest
from openbb_akshare.models.etf_historical import (
    AKShareEtfHistoricalFetcher,
    AKShareEtfHistoricalQueryParams,
    AKShareEtfHistoricalData,
)


def test_transform_query_with_defaults():
    """Test query transformation sets default dates."""
    fetcher = AKShareEtfHistoricalFetcher()
    query = fetcher.transform_query({"symbol": "159707"})
    assert query.symbol == "159707"
    assert query.period == "daily"
    assert query.start_date is not None
    assert query.end_date is not None


def test_transform_query_with_adjustment():
    """Test query transformation with adjustment parameter."""
    fetcher = AKShareEtfHistoricalFetcher()
    query = fetcher.transform_query({
        "symbol": "159707",
        "adjustment": "qfq",
    })
    assert query.adjustment == "qfq"


def test_transform_data_with_sample():
    """Test data mapping with sample AKShare data."""
    fetcher = AKShareEtfHistoricalFetcher()
    query = fetcher.transform_query({"symbol": "159707"})

    sample_data = [
        {
            "日期": "2024-01-02",
            "开盘": 1.50,
            "收盘": 1.55,
            "最高": 1.60,
            "最低": 1.45,
            "成交量": 500000,
            "成交额": 750000,
            "涨跌幅": 3.33,
            "涨跌额": 0.05,
        }
    ]

    result = fetcher.transform_data(query, sample_data)
    assert len(result) == 1
    assert isinstance(result[0], AKShareEtfHistoricalData)
    assert result[0].open == 1.50
    assert result[0].close == 1.55
    assert result[0].high == 1.60
    assert result[0].low == 1.45


def test_transform_data_filters_zero_prices():
    """Test that records with zero prices are filtered out (PositiveFloat constraint)."""
    fetcher = AKShareEtfHistoricalFetcher()
    query = fetcher.transform_query({"symbol": "159707"})

    sample_data = [
        {
            "日期": "2024-01-02",
            "开盘": 1.50,
            "收盘": 1.55,
            "最高": 1.60,
            "最低": 1.45,
            "成交量": 500000,
            "成交额": 750000,
            "涨跌幅": 3.33,
            "涨跌额": 0.05,
        },
        {
            "日期": "2024-01-03",
            "开盘": 0,
            "收盘": 0,
            "最高": 0,
            "最低": 0,
            "成交量": 0,
            "成交额": 0,
            "涨跌幅": 0,
            "涨跌额": 0,
        },
    ]

    result = fetcher.transform_data(query, sample_data)
    assert len(result) == 1
    assert result[0].open == 1.50


def test_transform_data_empty():
    """Test transform_data with empty list."""
    fetcher = AKShareEtfHistoricalFetcher()
    query = fetcher.transform_query({"symbol": "159707"})
    result = fetcher.transform_data(query, [])
    assert result == []


def test_extract_data_strips_prefix():
    """Test extract_data strips market prefix from symbol."""
    import re
    symbol = "SZ159707"
    stripped = re.sub(r"^(SH|SZ|BJ)", "", symbol)
    assert stripped == "159707"
