import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from analytics import kpis
import pandas as pd

def test_kpi_calculation():
    o = pd.DataFrame({
        "otif":[True, False],
        "fill_rate":[1.0, .5],
        "lead_time_days":[4, 6]
    })
    i = pd.DataFrame({"current_stock":[50], "reorder_point":[100]})
    result = kpis(o, i)
    assert result["OTIF %"] == 50.0
    assert result["At-Risk SKUs"] == 1
