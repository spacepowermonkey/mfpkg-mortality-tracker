import cairosvg
import datetime
import matplotlib.figure as figure



XTICK_YEARS = (
    [1, 53, 105],
    ["2020", "2021", "2022"]
)

XTICK_NONE = (
    [],
    []
)

YTICK_PERCENTS = (
    (-0.3, 1),
    [-0.2, -0.1, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    ["-20%", "-10%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%"],
    "% of All-Cause Mortality"
)

YTICK_2LOG = (
    (-5, 5),
    [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
    ["non-COVID", "1:16", "1:8", "1:4", "1:2", "1:1", "2:1", "4:1", "8:1", "16:1", "COVID"],
    None
)



def _save_image(fig, path_prefix):
    fig.savefig(f"{path_prefix}.svg")
    cairosvg.svg2png(
        file_obj=open(f"{path_prefix}.svg", "rb"), write_to=f"{path_prefix}.png"
    )
    return

def _shaded_composite(ax, mortality_df, key, title, color, xconf, yconf):
    xticks, xlabels = xconf
    ylimits, yticks, ylabels, ylabel = yconf

    mortality_by_country = mortality_df.groupby(by="country")
    for country in mortality_by_country:
        name, data = country
        rel_harm = data[key].to_numpy()

        ax.fill_between(list(range(len(rel_harm))), rel_harm, color=color, alpha=0.1)

    for level in yticks:
        ax.axhline(y=level, color="#000000", linewidth=0.5, linestyle=(0, (1, 10)))
    ax.axhline(y=0, color="#000000", linewidth=1)


    ax.axvline(x=52, color="#000000", linewidth=1, linestyle="dashed")
    ax.axvline(x=104, color="#000000", linewidth=1, linestyle="dashed")


    ax.set_title(title)
    if ylabel is not None:
        ax.set_ylabel(ylabel, rotation="vertical")

    ax.set_xticks(xticks, labels=xlabels)    
    ax.set_ylim(ylimits[0], ylimits[1])
    ax.set_yticks(yticks, labels=ylabels)
    ax.tick_params(labelbottom=True, bottom=False, labelleft=True, left=False, labelright=True, right=False)


    return



def run(mortality_df):
    fig = figure.Figure(figsize=(17, 11), dpi=300)
    ax_text = fig.add_axes([0,0,1,1])
    ax_excess = fig.add_axes([0.1,0.73,0.8,0.17])
    ax_covid = fig.add_axes([0.1,0.53,0.8,0.17])
    ax_nce = fig.add_axes([0.1,0.33,0.8,0.17])
    ax_rel = fig.add_axes([0.1,0.12,0.8,0.17])


    ax_text.text(0.05, 0.93, "COVID Mortality Overview", fontsize=24)
    ax_text.text(0.05, 0.06, "Source: OECD COVID-19 Health Indicators - Weekly Mortality")
    ax_text.text(0.05, 0.04, "https://stats.oecd.org/index.aspx?queryid=104676")
    ax_text.text(0.85, 0.04, f"Rendered on {datetime.date.today()}")

    _shaded_composite(ax_excess, mortality_df, "n_excess",
        "Excess Mortality", "#DC267F", xconf=XTICK_NONE, yconf=YTICK_PERCENTS)
    _shaded_composite(ax_covid, mortality_df, "n_covid",
        "COVID Mortality", "#FE6100", xconf=XTICK_NONE, yconf=YTICK_PERCENTS)
    _shaded_composite(ax_nce, mortality_df, "n_nce",
        "non-COVID Excess Mortality", "#648FFF", xconf=XTICK_NONE, yconf=YTICK_PERCENTS)
    _shaded_composite(ax_rel, mortality_df, "n_rel_mort",
        "Relative COVID to non-COVID Excess Mortality", "#785EF0", xconf=XTICK_YEARS, yconf=YTICK_2LOG)


    _save_image(fig, "/docs/covid-mortality")

    return
