import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from urllib.parse import urlparse

# ============================================================
# IRAPUATO, REIMAGINED
# Streamlit website powered by the FIRST worksheet ("Data")
# of IRAPUATO_REIMAGINED_Database.xlsx
# ============================================================

st.set_page_config(
    page_title="IRAPUATO, REIMAGINED",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- EDIT THESE TWO SETTINGS ----------
DATABASE_FILE = "IRAPUATO_REIMAGINED_Database.xlsx"
YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v=e0cehcrWnb8"
# Replace the URL above with your real, public or unlisted YouTube video URL.
# ---------------------------------------------

# Visual identity
DARK = "#111111"
LIME = "#B4F542"
OFFWHITE = "#F5F5F2"
GRAY = "#A7A7A2"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; }}
    .stApp {{ background: {OFFWHITE}; color: {DARK}; }}
    h1, h2, h3 {{ font-family: 'Barlow Condensed', sans-serif !important; text-transform: uppercase; letter-spacing: -1px; }}
    .hero {{
        background: linear-gradient(115deg, rgba(0,0,0,.94), rgba(0,0,0,.68)),
                    radial-gradient(circle at 80% 20%, #526c20, #111 65%);
        padding: 4.5rem 3rem; border-radius: 22px; color: white;
        min-height: 360px; display:flex; flex-direction:column; justify-content:center;
        border: 1px solid #252525;
    }}
    .hero-kicker {{ color:{LIME}; font-weight:700; letter-spacing:3px; font-size:.8rem; }}
    .hero-title {{ font-family:'Barlow Condensed',sans-serif; font-size:clamp(3.8rem,9vw,8rem);
        line-height:.82; font-weight:900; margin:.6rem 0; color:white; }}
    .hero-sub {{ color:#e9e9e4; font-size:1.1rem; max-width:680px; }}
    .lime {{ color:{LIME}; }}
    .eyebrow {{ color:#536d1e; letter-spacing:2px; font-size:.75rem; font-weight:800; }}
    .section-card {{ background:white; padding:1.2rem 1.35rem; border-radius:16px;
        border:1px solid #e4e4de; height:100%; }}
    .metric-note {{ color:#62625d; font-size:.85rem; }}
    .source-line {{ color:#666; font-size:.78rem; }}
    .scenario-box {{ background:#151515; color:white; padding:1.5rem; border-radius:18px; }}
    .scenario-box h3 {{ color:{LIME}; }}
    div[data-testid="stMetric"] {{ background:white; border:1px solid #e5e5df;
        padding:14px 16px; border-radius:14px; }}
    div[data-testid="stMetricLabel"] p {{ font-weight:700; }}
    .stButton button {{ border-radius:999px; font-weight:700; }}
    .stTabs [data-baseweb="tab-list"] {{ gap:8px; }}
    .stTabs [data-baseweb="tab"] {{ border-radius:999px; padding:8px 16px; }}
    a {{ color:#48651b !important; font-weight:700; }}
    footer {{visibility:hidden;}}
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_database(path_string: str) -> pd.DataFrame:
    path = Path(path_string)
    if not path.exists():
        raise FileNotFoundError(
            f"Could not find {path.name}. Put the Excel file in the same folder as app.py."
        )
    # IMPORTANT: Read only the first worksheet, named "Data".
    data = pd.read_excel(path, sheet_name=0)
    required = ["ID", "Section", "Topic", "Information", "Source", "Link"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        raise ValueError(f"The first worksheet is missing these columns: {', '.join(missing)}")
    data = data[required].dropna(subset=["Topic", "Information"]).copy()
    data["Section"] = data["Section"].astype(str).str.strip()
    data["Topic"] = data["Topic"].astype(str).str.strip()
    data["Information"] = data["Information"].astype(str).str.strip()
    data["Source"] = data["Source"].fillna("Source not specified").astype(str)
    data["Link"] = data["Link"].fillna("").astype(str)
    return data

try:
    db = load_database(DATABASE_FILE)
except Exception as error:
    st.error(f"Database loading error: {error}")
    st.info("Check that app.py and IRAPUATO_REIMAGINED_Database.xlsx are saved in the same folder.")
    st.stop()

def get_record(topic_fragment: str):
    match = db[db["Topic"].str.contains(topic_fragment, case=False, na=False)]
    return match.iloc[0] if not match.empty else None

def content_card(record, show_source=True):
    if record is None:
        return
    st.markdown(f"### {record['Topic']}")
    st.write(record["Information"])
    if show_source:
        st.caption(f"Source: {record['Source']}")
        if str(record["Link"]).startswith("http"):
            st.markdown(f"[OPEN SOURCE ↗]({record['Link']})")

def records_for(section):
    return db[db["Section"].str.lower() == section.lower()]

# Supplemental photos: these are decorative and do not alter the database copy.
PHOTO = {
    "home": "https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=1800&q=85",
    "water": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?auto=format&fit=crop&w=1200&q=85",
    "green": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=85",
    "city": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?auto=format&fit=crop&w=1200&q=85",
    "waste": "https://images.unsplash.com/photo-1532996122724-6d9b2b7d9d3a?auto=format&fit=crop&w=1200&q=85",
    "climate": "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1200&q=85",
    "future": "https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=1800&q=85",
    "action": "https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?auto=format&fit=crop&w=1400&q=85",
    "impact": "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1400&q=85",
}

# Navigation
nav_items = ["HOME", "THE CHALLENGE", "THE FUTURE", "THE CHANGE", "YOUR IMPACT", "ABOUT US"]
selected = st.radio("NAVIGATION", nav_items, horizontal=True, label_visibility="collapsed")

# ---------------- HOME ----------------
if selected == "HOME":
    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-kicker">A LOCAL PROJECT. A SHARED FUTURE.</div>
          <div class="hero-title">IRAPUATO,<br><span class="lime">REIMAGINED.</span></div>
          <div class="hero-sub">What could our city become by 2050? Explore the challenges,
          compare possible futures, and discover how today's decisions can shape tomorrow.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image(PHOTO["home"], use_container_width=True)
    st.write("")
    concept = get_record("project concept")
    goal = get_record("Project goal")
    c1, c2 = st.columns([1.15, 1])
    with c1:
        st.markdown('<div class="eyebrow">THE IDEA</div>', unsafe_allow_html=True)
        content_card(concept)
    with c2:
        st.markdown('<div class="eyebrow">WHY IT MATTERS</div>', unsafe_allow_html=True)
        content_card(goal)
    st.markdown("## THREE CONNECTED GOALS")
    sdg_records = records_for("SDGs")
    cols = st.columns(3)
    for col, fragment in zip(cols, ["SDG 6", "SDG 11", "SDG 13"]):
        row = sdg_records[sdg_records["Topic"].str.contains(fragment, case=False, na=False)]
        with col:
            if not row.empty:
                content_card(row.iloc[0], show_source=True)
    st.caption("Independent educational project. Not an official municipal government website.")


# ---------------- THE CHALLENGE ----------------
elif selected == "THE CHALLENGE":
    st.markdown('<div class="eyebrow">02 / UNDERSTAND THE PRESENT</div>', unsafe_allow_html=True)
    st.title("OUR CITY. OUR CHALLENGES.")
    st.write("Explore local information about water, urban development, green spaces, waste, and environmental resilience.")

    st.image(PHOTO["city"], use_container_width=True)

    local = records_for("Local Context")

    topic_filter = st.selectbox(
        "Explore a topic",
        [
            "All local topics",
            "Water",
            "Green spaces & biodiversity",
            "Urban planning",
            "Air quality & waste",
            "Climate & resilience"
        ],
    )

    if topic_filter == "Water":
        filtered = local[local["Topic"].str.contains(
            "water|groundwater|aquifer", case=False, na=False
        )]

    elif topic_filter == "Green spaces & biodiversity":
        filtered = local[local["Topic"].str.contains(
            "green|park|protected|vegetation|biodiversity|natural",
            case=False, na=False
        )]

    elif topic_filter == "Urban planning":
        filtered = local[local["Topic"].str.contains(
            "urban|mobility|territorial|participatory",
            case=False, na=False
        )]

    elif topic_filter == "Air quality & waste":
        filtered = local[local["Topic"].str.contains(
            "air|waste|plastic|burning", case=False, na=False
        )]

    elif topic_filter == "Climate & resilience":
        filtered = local[local["Topic"].str.contains(
            "climate|resilien|risk", case=False, na=False
        )]

    else:
        filtered = local

    # Topic-specific images
    topic_photo = {
        "All local topics": PHOTO["city"],
        "Water": PHOTO["water"],
        "Green spaces & biodiversity": PHOTO["green"],
        "Urban planning": PHOTO["city"],
        "Air quality & waste": PHOTO["waste"],
        "Climate & resilience": PHOTO["climate"],
    }

    st.image(topic_photo[topic_filter], use_container_width=True)

    # Display local information
    for start in range(0, len(filtered), 2):
        cols = st.columns(2)

        for col, (_, row) in zip(
            cols, filtered.iloc[start:start+2].iterrows()
        ):
            with col:
                with st.container(border=True):
                    content_card(row)

    st.markdown("---")
    st.markdown("## LOCAL EVIDENCE / INTERACTIVE DATA")

    st.write(
        "Explore the reported figures below. Hover over bars or slices "
        "for details. Each chart retains the source year and context."
    )

    # Create chart tabs
    chart_tabs = st.tabs([
        "WATER COVERAGE",
        "WATER VOLUMES",
        "WELLS",
        "VEGETATION"
    ])

    # CHART 1: WATER COVERAGE
    with chart_tabs[0]:

        coverage_df = pd.DataFrame({
            "Area": ["Municipality", "Rural areas"],
            "Coverage (%)": [98.61, 94.94]
        })

        fig = px.bar(
            coverage_df,
            x="Area",
            y="Coverage (%)",
            text="Coverage (%)",
            range_y=[0, 105],
            title="Water-service coverage · Census 2020",
            hover_data={"Coverage (%)": ":.2f"}
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        fig.update_layout(
            template="plotly_white",
            yaxis_title="Coverage (%)",
            xaxis_title="",
            showlegend=False,
            margin=dict(l=20, r=20, t=65, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": True}
        )

        record = get_record("Water service coverage")

        if record is not None:
            st.caption(
                f"Source: {record['Source']} · {record['Information']}"
            )

    # CHART 2: WATER VOLUMES
    with chart_tabs[1]:

        volume_df = pd.DataFrame({
            "Measure": ["Annual extraction", "Concession volume"],
            "Volume (hm³/year)": [37.0, 58.3]
        })

        fig = px.bar(
            volume_df,
            x="Measure",
            y="Volume (hm³/year)",
            text="Volume (hm³/year)",
            title="Groundwater volumes cited for 2020",
            hover_data={"Volume (hm³/year)": ":.1f"}
        )

        fig.update_traces(
            texttemplate="%{text:.1f} hm³",
            textposition="outside"
        )

        fig.update_layout(
            template="plotly_white",
            yaxis_title="hm³/year",
            xaxis_title="",
            showlegend=False,
            margin=dict(l=20, r=20, t=65, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": True}
        )

        record = get_record("Water extraction data")

        if record is not None:
            st.caption(
                f"Source: {record['Source']} · {record['Information']}"
            )

    # CHART 3: WELLS
    with chart_tabs[2]:

        wells_df = pd.DataFrame({
            "Status": [
                "Operating",
                "Reserve",
                "Out of operation"
            ],
            "Wells": [81, 10, 11]
        })

        fig = px.pie(
            wells_df,
            names="Status",
            values="Wells",
            hole=0.52,
            title="Well status reported in the municipal document",
            hover_data={"Wells": True}
        )

        fig.update_traces(
            textinfo="label+percent",
            sort=False
        )

        fig.update_layout(
            template="plotly_white",
            margin=dict(l=20, r=20, t=65, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": True}
        )

        record = get_record("Water extraction data")

        if record is not None:
            st.caption(
                f"Source: {record['Source']} · {record['Information']}"
            )

    # CHART 4: VEGETATION
    with chart_tabs[3]:

        vegetation_df = pd.DataFrame({
            "Period": ["2000–2018"],
            "Reported change (%)": [-15]
        })

        fig = px.bar(
            vegetation_df,
            x="Period",
            y="Reported change (%)",
            text="Reported change (%)",
            title="Reported forest-vegetation area change · 2000–2018",
            hover_data={"Reported change (%)": True}
        )

        fig.update_traces(
            texttemplate="%{text:.0f}%",
            textposition="outside"
        )

        fig.update_layout(
            template="plotly_white",
            yaxis_title="Reported change (%)",
            xaxis_title="",
            margin=dict(l=20, r=20, t=65, b=20)
        )

        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="#777"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": True}
        )

        record = get_record("Vegetation loss")

        if record is not None:
            st.caption(
                f"Source: {record['Source']} · {record['Information']}"
            )

    st.info(
        "Historical figures from cited documents only — "
        "not live data or updated 2026 measurements."
    )

# ---------------- THE FUTURE ----------------
elif selected == "THE FUTURE":
    st.markdown('<div class="eyebrow">03 / EXPLORE POSSIBLE TOMORROWS</div>', unsafe_allow_html=True)
    st.title("IRAPUATO FUTURE EXPLORER")
    st.write("Change the priorities below and explore two different pathways for the city. Your selections shape the experience, not a scientific forecast.")
    st.image(PHOTO["future"], use_container_width=True)
    st.warning("This is an educational scenario explorer. Its controls are illustrative and do not calculate official predictions, future percentages, or real municipal outcomes.")

    scenario = st.segmented_control(
        "Choose a possible future",
        options=["FUTURE A · SUSTAINABLE DECISIONS", "FUTURE B · CHALLENGES CONTINUE"],
        default="FUTURE A · SUSTAINABLE DECISIONS",
    )
    st.markdown("### BUILD YOUR 2050 PRIORITIES")
    st.caption("Move the sliders to decide how strongly each topic should be prioritized in the future you want to explore.")
    a, b, c = st.columns(3)
    with a:
        water = st.slider("Water stewardship", 0, 100, 75, 5, help="Your chosen priority for conservation, efficient use, treatment and reuse.")
    with b:
        green = st.slider("Green & public spaces", 0, 100, 75, 5, help="Your chosen priority for parks, natural areas and accessible public spaces.")
    with c:
        resilience = st.slider("Climate resilience", 0, 100, 75, 5, help="Your chosen priority for adaptation, preparedness and resilient infrastructure.")

    priority_df = pd.DataFrame({
        "Priority": ["Water stewardship", "Green & public spaces", "Climate resilience"],
        "Your selected priority": [water, green, resilience],
    })
    radar = go.Figure()
    radar.add_trace(go.Scatterpolar(
        r=[water, green, resilience, water],
        theta=["Water", "Green spaces", "Climate resilience", "Water"],
        fill="toself", name="Your priorities",
        line=dict(color="#769F25", width=3),
    ))
    radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], ticksuffix="%")),
        showlegend=False, template="plotly_white", title="Your chosen priorities for 2050",
        margin=dict(l=35, r=35, t=65, b=35),
    )
    left, right = st.columns([1.05, 1])
    with left:
        st.plotly_chart(radar, use_container_width=True, config={"displayModeBar": True})
    with right:
        if scenario.startswith("FUTURE A"):
            st.markdown('<div class="scenario-box"><div class="eyebrow">FUTURE A</div><h3>A BETTER TOMORROW</h3><p>What if Irapuato strengthens sustainable planning and community action?</p></div>', unsafe_allow_html=True)
            content_card(get_record("Scenario A — Irapuato with sustainable decisions"), show_source=True)
            st.markdown("**How your selected priorities could shape this pathway:**")
            if water >= 60:
                st.write("💧 Water receives strong attention: conservation, efficient use, treatment, and reuse are central priorities.")
            else:
                st.write("💧 Water is a lower priority in your selected pathway; the city may need stronger efforts in this area.")
            if green >= 60:
                st.write("🌳 Green and public spaces receive strong attention: parks, natural areas, and access are emphasized.")
            else:
                st.write("🌳 Green spaces receive less emphasis in your selected pathway.")
            if resilience >= 60:
                st.write("🌦️ Climate resilience is emphasized through adaptation, preparedness, and planning.")
            else:
                st.write("🌦️ Climate resilience receives less emphasis in your selected pathway.")
        else:
            st.markdown('<div class="scenario-box"><div class="eyebrow">FUTURE B</div><h3>A WORLD UNCHANGED</h3><p>What if current challenges continue because action is insufficient or inconsistent?</p></div>', unsafe_allow_html=True)
            content_card(get_record("Scenario B — Challenges continue"), show_source=True)
            st.markdown("**Areas that may remain under pressure in this illustrative pathway:**")
            if water < 60:
                content_card(get_record("Scenario B — Indicator: Water pressure"), show_source=False)
            if green < 60:
                content_card(get_record("Scenario B — Indicator: Green-space pressure"), show_source=False)
            if resilience < 60:
                content_card(get_record("Scenario B — Indicator: Environmental resilience"), show_source=False)
            if min(water, green, resilience) >= 60:
                st.write("Your selected priorities are all high. This makes the contrast especially clear: sustained implementation and resources would still be needed to move from priorities to real outcomes.")
    st.markdown("---")
    st.markdown("### COMPARE THE PATHWAYS")
    compare = st.columns(2)
    with compare[0]:
        st.markdown("**FUTURE A — SUSTAINABLE DECISIONS**")
        content_card(get_record("Scenario A — Indicator: Water stewardship"), show_source=False)
        content_card(get_record("Scenario A — Indicator: Green and public spaces"), show_source=False)
        content_card(get_record("Scenario A — Indicator: Climate and environmental resilience"), show_source=False)
    with compare[1]:
        st.markdown("**FUTURE B — CHALLENGES CONTINUE**")
        content_card(get_record("Scenario B — Indicator: Water pressure"), show_source=False)
        content_card(get_record("Scenario B — Indicator: Green-space pressure"), show_source=False)
        content_card(get_record("Scenario B — Indicator: Environmental resilience"), show_source=False)
    st.caption("Scenario descriptions are qualitative and based on the database's cited municipal planning documents and SDG references. They are not measured forecasts.")

# ---------------- THE CHANGE ----------------
elif selected == "THE CHANGE":
    st.markdown('<div class="eyebrow">04 / TURN IDEAS INTO ACTION</div>', unsafe_allow_html=True)
    st.title("THE FUTURE DOESN'T CHANGE BY ITSELF.")
    st.write("Explore realistic actions that residents, schools, communities, organizations, and institutions can take.")
    actions = records_for("Take Action")
    for _, row in actions.iterrows():
        with st.expander(row["Topic"]):
            st.write(row["Information"])
            st.caption(f"Source: {row['Source']}")
            if str(row["Link"]).startswith("http"):
                st.markdown(f"[LEARN MORE ↗]({row['Link']})")

# ---------------- YOUR IMPACT ----------------
elif selected == "YOUR IMPACT":
    st.markdown('<div class="eyebrow">05 / YOUR CHOICE MATTERS</div>', unsafe_allow_html=True)
    st.title("WHAT FUTURE WILL YOU HELP CREATE?")
    st.write("Choose one realistic commitment. This is a personal reflection activity, not a measurement of your environmental impact.")
    commitments = [
        "I will learn more about water in my community.",
        "I will reduce unnecessary waste.",
        "I will help care for shared green spaces.",
        "I will share reliable information about a local issue.",
        "I will learn how to participate in my community.",
    ]
    chosen = st.multiselect("MY COMMITMENTS", commitments, max_selections=3)
    if chosen:
        st.success("YOUR IRAPUATO, REIMAGINED COMMITMENT")
        for item in chosen:
            st.write(f"✓ {item}")
        st.caption("Small actions can contribute to change. Structural challenges also require planning, public services, investment, and collective responsibility.")
    else:
        st.info("Select one or more commitments to create your personal action list.")
    content_card(get_record("Change requires collaboration"))

# ---------------- ABOUT US ----------------
elif selected == "ABOUT US":
    st.markdown('<div class="eyebrow">06 / THE PEOPLE BEHIND THE PROJECT</div>', unsafe_allow_html=True)
    st.title("MEET THE TEAM.")
    st.image(PHOTO["green"], use_container_width=True)
    content_card(get_record("About the project"))
    st.markdown("## OUR STORY")
    st.write("We chose Irapuato because the future of a city begins with understanding the place we call home. Through research, data, and interactive storytelling, we want to make local sustainability challenges easier to explore and discuss.")
    st.markdown("## MEET US")
    content_card(get_record("Project team"))
    st.markdown("## OUR VIDEO")
    # Streamlit handles YouTube links directly. Use the canonical watch URL.
    st.video("https://www.youtube.com/watch?v=e0cehcrWnb8")
    st.markdown("[OPEN VIDEO ON YOUTUBE ↗](https://youtu.be/e0cehcrWnb8)")
    st.markdown("## SOURCES & TRANSPARENCY")
    for _, row in db[["Source", "Link"]].drop_duplicates().iterrows():
        if str(row["Link"]).startswith("http"):
            st.markdown(f"- [{row['Source']}]({row['Link']})")
    for fragment in ["Scenario disclaimer", "Local data disclaimer", "Source and attribution policy"]:
        content_card(get_record(fragment))

# Footer
st.markdown("---")
st.markdown(
    f"<div style='display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;color:#666;font-size:.8rem'>"
    f"<span><b>IRAPUATO, REIMAGINED.</b> · THE FUTURE IS OURS.</span>"
    f"<span>Educational project · Data and scenarios are source-attributed</span></div>",
    unsafe_allow_html=True,
)
