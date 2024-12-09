import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load dataset with caching
@st.cache_data
def load_data():
    return pd.read_csv("Shark Tank India.csv")

# Load the data
data = load_data()

# Clean and standardize column names
data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')

# Sidebar Navigation
st.sidebar.title("Navigation")
pages = st.sidebar.radio("Go to", ["Home", "Industry Analysis", "Shark Participation"])

# Page: Home
if pages == "Home":
    st.title("Shark Tank India - Data Analysis")
    st.write("This app provides an analysis of Shark Tank India data.")
    
    # Overview Metrics
    st.header("Overall Metrics")
    total_startups = data["startup_name"].nunique() if "startup_name" in data.columns else "N/A"
    total_industries = data["industry"].nunique() if "industry" in data.columns else "N/A"
    total_seasons = data["season_number"].nunique() if "season_number" in data.columns else "N/A"
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Startups", total_startups)
    col2.metric("Industries", total_industries)
    col3.metric("Seasons", total_seasons)

    # Plot: Startups by Season
    if "season_number" in data.columns:
        st.subheader("Startups by Season")
        startups_by_season = data["season_number"].value_counts().sort_index()
        fig, ax = plt.subplots()
        sns.barplot(
            x=startups_by_season.index.astype(str),
            y=startups_by_season.values,
            ax=ax,
            hue=startups_by_season.index.astype(str),
            dodge=False,
            palette=sns.color_palette("viridis", len(startups_by_season))
        )
        if ax.legend_:  # Check if the legend exists
            ax.legend_.remove()
        ax.set_xlabel("Season")
        ax.set_ylabel("Number of Startups")
        ax.set_title("Number of Startups per Season")
        st.pyplot(fig)
    else:
        st.warning("The column 'season_number' is not available in the dataset.")

# Page: Industry Analysis
elif pages == "Industry Analysis":
    st.title("Industry Analysis")
    
    # Industry Distribution
    if "industry" in data.columns:
        st.subheader("Startups by Industry")
        industry_counts = data["industry"].value_counts()

        # Bar Chart for Industry Distribution
        fig = px.bar(
            x=industry_counts.index,
            y=industry_counts.values,
            title="Industry Distribution",
            labels={"x": "Industry", "y": "Number of Startups"},
            color=industry_counts.index,  # Optional: Add color by industry
            text=industry_counts.values   # Show counts on bars
        )
        fig.update_traces(textposition="outside", marker=dict(line=dict(color='black', width=1)))
        fig.update_layout(xaxis_title="Industry", yaxis_title="Number of Startups", showlegend=False)
        st.plotly_chart(fig)
    else:
        st.warning("The column 'industry' is not available in the dataset.")

    # Industry Trends by Season
    if "season_number" in data.columns and "industry" in data.columns:
        st.subheader("Popular Industries by Season")
        industry_trends = data.groupby(["season_number", "industry"]).size().reset_index(name="Count")
        fig = px.bar(industry_trends, x="season_number", y="Count", color="industry", barmode="stack")
        fig.update_layout(xaxis_title="Season", yaxis_title="Number of Startups")
        st.plotly_chart(fig)
    else:
        st.warning("Columns 'season_number' and/or 'industry' are not available in the dataset.")

# Page: Shark Participation
elif pages == "Shark Participation":
    st.title("Shark Participation")
    
    # Shark Investments
    shark_columns = ["namita_present", "vineeta_present", "anupam_present", "aman_present", "peyush_present", "amit_present", "ashneer_present"]
    available_shark_columns = [col for col in shark_columns if col in data.columns]

    if available_shark_columns:
        st.subheader("Shark Investment Count")
        shark_investments = data[available_shark_columns].sum().reset_index()
        shark_investments.columns = ["Shark", "Investments"]
        fig = px.bar(shark_investments, x="Shark", y="Investments", title="Shark Investments")
        fig.update_layout(xaxis_title="Shark", yaxis_title="Number of Investments")
        st.plotly_chart(fig)

        # Shark Participation by Industry
        st.subheader("Shark Participation by Industry")
        shark_industry = data.groupby("industry")[available_shark_columns].sum()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(shark_industry, annot=True, fmt="g", cmap="YlGnBu", ax=ax)
        ax.set_title("Shark Participation by Industry")
        st.pyplot(fig)
    else:
        st.warning("No shark-related columns are available in the dataset.")

