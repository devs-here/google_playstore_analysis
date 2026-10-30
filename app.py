from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Google Play Store Analysis", layout="wide")

data_dir = Path(__file__).resolve().parent / "app_data"


@st.cache_data
def load(name):
    return pd.read_csv(data_dir / f"{name}.csv")


st.title("Google Play Store Analysis")
st.caption("9,659 unique apps, cleaned with pandas and analysed in MySQL.")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Categories", "Free vs Paid", "Installs & Size", "Trends", "Top apps"]
)

# ---------- Tab 1: Categories ----------
with tab1:
    cats = load("categories")
    min_rated = st.slider("Minimum rated apps per category", 0, 300, 50, step=10)
    shown = cats[cats["rated_apps"] >= min_rated]

    c1, c2, c3 = st.columns(3)
    c1.metric("Apps", f"{cats['total_apps'].sum():,}")
    c2.metric("Categories shown", len(shown))
    c3.metric("Share with a rating", f"{100 * cats['rated_apps'].sum() / cats['total_apps'].sum():.0f}%")

    left, right = st.columns(2)
    with left:
        fig = px.bar(
            shown.sort_values("avg_rating"),
            x="avg_rating", y="category", orientation="h",
            title="Average rating by category",
            labels={"avg_rating": "Average rating", "category": ""},
        )
        fig.update_xaxes(range=[3.8, 4.5])
        fig.update_yaxes(dtick=1)
        fig.update_layout(height=max(400, 28 * len(shown)))
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.scatter(
            shown, x="total_apps", y="avg_rating", hover_name="category",
            title="Rating vs number of apps (competition)",
            labels={"total_apps": "Total apps", "avg_rating": "Average rating"},
        )
        st.plotly_chart(fig, use_container_width=True)
    st.caption("The rating axis starts at 3.8, so small differences look bigger than they are.")

# ---------- Tab 2: Free vs Paid ----------
with tab2:
    fp = load("free_paid")
    st.dataframe(fp, hide_index=True, use_container_width=True)
    cols = st.columns(3)
    for col, metric, title in zip(
        cols,
        ["avg_rating", "avg_reviews", "avg_installs"],
        ["Average rating", "Average reviews", "Average installs (min)"],
    ):
        with col:
            fig = px.bar(fp, x="type", y=metric, title=title, labels={"type": ""})
            st.plotly_chart(fig, use_container_width=True)
    st.caption("Averages are pulled up by a few giant apps, so the typical app is much smaller.")

    heat = load("rating_heatmap")
    pivot = heat.pivot(index="category", columns="install_range", values="avg_rating")
    fig = px.imshow(
        pivot, aspect="auto", text_auto=".2f",
        color_continuous_scale="RdYlGn", zmin=3.6, zmax=4.6,
        title="Average rating by category and install range",
        labels={"color": "Avg rating", "x": "", "y": ""},
    )
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Blank cells have fewer than 10 rated apps.")

# ---------- Tab 3: Installs & Size ----------
with tab3:
    inst = load("install_ranges")
    size = load("size_ranges")
    left, right = st.columns(2)
    with left:
        fig = px.bar(inst, x="install_range", y="avg_rating", title="Rating by install range",
                     labels={"install_range": "", "avg_rating": "Average rating"})
        fig.update_yaxes(range=[3.8, 4.6])
        st.plotly_chart(fig, use_container_width=True)
        fig = px.bar(inst, x="install_range", y="avg_reviews", title="Reviews by install range",
                     labels={"install_range": "", "avg_reviews": "Average reviews"})
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.bar(size, x="size_range", y="avg_rating", title="Rating by app size",
                     labels={"size_range": "", "avg_rating": "Average rating"})
        fig.update_yaxes(range=[3.8, 4.6])
        st.plotly_chart(fig, use_container_width=True)
        fig = px.bar(size, x="size_range", y="avg_installs", title="Installs (min) by app size",
                     labels={"size_range": "", "avg_installs": "Average installs"})
        st.plotly_chart(fig, use_container_width=True)
    st.caption("Size excludes apps listed as 'Varies with device'.")

# ---------- Tab 4: Trends ----------
with tab4:
    yr = load("update_year")
    yr = yr[yr["update_year"] >= 2013]
    fig = px.line(yr, x="update_year", y="avg_rating", markers=True,
                  title="Average rating by last update year",
                  labels={"update_year": "Year", "avg_rating": "Average rating"})
    fig.update_yaxes(range=[3.8, 4.5])
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Years before 2013 are left out because they have very few apps.")

    cr = load("content_rating")
    cr = cr[cr["rated_apps"] >= 50]
    left, right = st.columns(2)
    with left:
        fig = px.bar(cr, x="content_rating", y="avg_rating", title="Rating by content rating",
                     labels={"content_rating": "", "avg_rating": "Average rating"})
        fig.update_yaxes(range=[3.8, 4.5])
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.bar(cr, x="content_rating", y="avg_installs", title="Installs (min) by content rating",
                     labels={"content_rating": "", "avg_installs": "Average installs"})
        st.plotly_chart(fig, use_container_width=True)
    st.caption("Content ratings with fewer than 50 rated apps (Adults only 18+, Unrated) are left out.")
# ---------- Tab 5: Top apps ----------
with tab5:
    left, right = st.columns(2)
    with left:
        st.subheader("Top 10 by reviews")
        st.dataframe(load("top_reviews"), hide_index=True, use_container_width=True)
    with right:
        st.subheader("Top 10 by installs")
        st.dataframe(load("top_installs"), hide_index=True, use_container_width=True)