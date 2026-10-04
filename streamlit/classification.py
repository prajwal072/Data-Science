import streamlit as st
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


st.set_page_config(page_title="Iris Field Guide", page_icon="🌿", layout="wide")


@st.cache_data
def load_data():
    iris = load_iris()
    features = pd.DataFrame(iris.data, columns=iris.feature_names)
    labels = pd.Series(iris.target, name="target")
    return iris, features, labels


@st.cache_resource
def train_model():
    iris, features, labels = load_data()
    train_features, test_features, train_labels, test_labels = train_test_split(
        features, labels, test_size=0.2, random_state=42, stratify=labels
    )
    evaluation_model = RandomForestClassifier(n_estimators=180, random_state=42)
    evaluation_model.fit(train_features, train_labels)
    accuracy = accuracy_score(test_labels, evaluation_model.predict(test_features))

    model = RandomForestClassifier(n_estimators=180, random_state=42)
    model.fit(features, labels)
    return model, accuracy


iris, features, labels = load_data()
model, accuracy = train_model()
species = list(iris.target_names)
dataset = features.assign(species=labels.map(dict(enumerate(species))))

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
    .stApp { background: #f5f5ef; color: #20352c; }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] { background: #e8eee5; border-right: 1px solid #d4dfd3; }
    [data-testid="stSidebar"] * { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3 { color: #20352c; }
    h1 { font-family: 'Playfair Display', Georgia, serif !important; font-size: 2.7rem !important; }
    p, label, [data-testid="stMetricValue"] { font-family: 'DM Sans', sans-serif; }
    .eyebrow { color: #597561; font: 700 0.75rem 'DM Sans', sans-serif; letter-spacing: 0.12em; text-transform: uppercase; }
    .intro { color: #64756a; font: 400 1rem 'DM Sans', sans-serif; margin: -0.6rem 0 1.4rem; }
    .stMetric { background: #fff; border: 1px solid #dce4da; border-radius: 6px; padding: 0.9rem 1rem; }
    [data-testid="stMetricLabel"] { color: #66796b; }
    [data-testid="stMetricValue"] { color: #244b38; }
    div[data-testid="stTabs"] button { color: #52685a; }
    div[data-testid="stTabs"] button[aria-selected="true"] { color: #24543b; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow">A pocket field guide to the Iris dataset</div>', unsafe_allow_html=True)
st.title("Read a flower by its measurements")
st.markdown(
    '<div class="intro">Adjust the specimen measurements and let a Random Forest compare them with 150 known irises.</div>',
    unsafe_allow_html=True,
)

st.sidebar.markdown("### Specimen measurements")
st.sidebar.caption("Set the sepal and petal dimensions in centimeters.")
versicolor_median = features.loc[labels == 1].median()
measurements = {}
for feature in features.columns:
    measurements[feature] = st.sidebar.slider(
        feature.replace(" (cm)", "").title(),
        min_value=float(features[feature].min()),
        max_value=float(features[feature].max()),
        value=float(versicolor_median[feature]),
        step=0.1,
        help="Measured in centimeters.",
    )

prediction = int(model.predict(pd.DataFrame([measurements]))[0])
probabilities = model.predict_proba(pd.DataFrame([measurements]))[0]
confidence = float(probabilities[prediction])

overview_tab, dataset_tab = st.tabs(["Identify a specimen", "Explore the dataset"])

with overview_tab:
    metric_cols = st.columns(3)
    metric_cols[0].metric("Predicted species", species[prediction].title())
    metric_cols[1].metric("Model confidence", f"{confidence:.0%}")
    metric_cols[2].metric("Validation accuracy", f"{accuracy:.0%}", help="Held-out test split; stratified, 80/20.")

    left, right = st.columns([1.05, 1.45], gap="large")
    with left:
        st.subheader("Confidence by species")
        probability_data = pd.DataFrame({"Species": [name.title() for name in species], "Probability": probabilities})
        st.bar_chart(probability_data, x="Species", y="Probability", color="#507c5e", height=265)
        st.caption("Confidence scores are model estimates, not calibrated probabilities.")

    with right:
        st.subheader("Petal profile")
        plotted_data = dataset[["petal length (cm)", "petal width (cm)", "species"]].copy()
        specimen = pd.DataFrame([{
            "petal length (cm)": measurements["petal length (cm)"],
            "petal width (cm)": measurements["petal width (cm)"],
            "species": "Your specimen",
        }])
        plotted_data = pd.concat([plotted_data, specimen], ignore_index=True)
        st.scatter_chart(
            plotted_data,
            x="petal length (cm)",
            y="petal width (cm)",
            color="species",
            height=330,
        )
        st.caption("Your specimen is shown alongside the 150 labeled flowers.")

with dataset_tab:
    st.subheader("The reference collection")
    counts = dataset["species"].value_counts()
    summary_cols = st.columns(3)
    for column, name in zip(summary_cols, species):
        column.metric(name.title(), f"{counts[name]} samples")

    importance = pd.DataFrame({"Feature": features.columns, "Importance": model.feature_importances_})
    importance = importance.sort_values("Importance", ascending=False)
    chart_col, table_col = st.columns([1, 1.2], gap="large")
    with chart_col:
        st.subheader("What the model weighs")
        st.bar_chart(importance, x="Feature", y="Importance", color="#c8794e", horizontal=True)
    with table_col:
        st.subheader("Sample measurements")
        st.dataframe(dataset, use_container_width=True, hide_index=True)