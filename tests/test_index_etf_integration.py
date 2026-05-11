"""Integration tests for Index and ETF models."""

import pytest
from openbb import obb
import pandas as pd


# --- IndexConstituents ---

@pytest.mark.parametrize("symbol", ["000300", "000905"])
def test_index_constituents(symbol, default_provider):
    """Test index constituents endpoint."""
    result = obb.index.constituents(symbol=symbol, provider=default_provider)
    df = result.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "symbol" in df.columns


# --- IndexSearch ---

@pytest.mark.parametrize("query", ["沪深", "上证"])
def test_index_search(query, default_provider):
    """Test index search endpoint."""
    result = obb.index.search(query=query, provider=default_provider)
    df = result.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_index_search_by_symbol(default_provider):
    """Test index search by symbol."""
    result = obb.index.search(query="000300", is_symbol=True, provider=default_provider)
    df = result.to_dataframe()
    assert isinstance(df, pd.DataFrame)


# --- IndexSnapshots ---

def test_index_snapshots_default(default_provider):
    """Test index snapshots with default category."""
    result = obb.index.snapshots(provider=default_provider)
    df = result.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "symbol" in df.columns
    assert "price" in df.columns


@pytest.mark.parametrize("category", ["上证系列指数", "深证系列指数"])
def test_index_snapshots_category(category, default_provider):
    """Test index snapshots with specific category."""
    result = obb.index.snapshots(
        provider=default_provider, category=category
    )
    df = result.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


# --- IndexHistorical ---

@pytest.mark.parametrize("symbol", ["000300", "000905"])
def test_index_historical(symbol, default_provider):
    """Test index historical endpoint."""
    result = obb.index.price.historical(
        symbol=symbol, provider=default_provider
    )
    df = result.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "open" in df.columns
    assert "close" in df.columns


@pytest.mark.parametrize("period", ["daily", "weekly", "monthly"])
def test_index_historical_period(period, default_provider):
    """Test index historical with different periods."""
    result = obb.index.price.historical(
        symbol="000300", provider=default_provider, period=period
    )
    df = result.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_index_historical_with_dates(default_provider):
    """Test index historical with date range."""
    result = obb.index.price.historical(
        symbol="000300",
        start_date="2024-01-01",
        end_date="2024-12-31",
        provider=default_provider,
    )
    df = result.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_index_historical_with_prefix(default_provider):
    """Test index historical strips market prefix."""
    result = obb.index.price.historical(
        symbol="SH000300", provider=default_provider
    )
    df = result.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


# --- EtfHistorical ---

@pytest.mark.parametrize("symbol", ["159919", "510300"])
def test_etf_historical(symbol, default_provider):
    """Test ETF historical endpoint."""
    result = obb.etf.historical(
        symbol=symbol, provider=default_provider
    )
    df = result.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "open" in df.columns
    assert "close" in df.columns


@pytest.mark.parametrize("adjustment", [None, "qfq", "hfq"])
def test_etf_historical_adjustment(adjustment, default_provider):
    """Test ETF historical with adjustment."""
    result = obb.etf.historical(
        symbol="159919",
        provider=default_provider,
        adjustment=adjustment,
    )
    df = result.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
