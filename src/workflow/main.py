from . import load_data
from . import mortality_stats
from . import render_charts

def run():
    mortality_df = load_data.run()
    mortality_df = mortality_stats.run(mortality_df)
    render_charts.run(mortality_df)

    print(mortality_df)
    return
