import pandas as pd
import pytest
from analytics import prepare_sales, metrics

def test_sales_metrics():
    raw = pd.DataFrame([dict(date='2026-01-01', region='East', category='Tech', product='Mouse', quantity=2, unit_price=10, unit_cost=4)])
    result = metrics(prepare_sales(raw))
    assert result['revenue'] == 20
    assert result['profit'] == 12
    assert result['margin'] == 60

def test_missing_columns():
    with pytest.raises(ValueError):
        prepare_sales(pd.DataFrame({'date': ['2026-01-01']}))
