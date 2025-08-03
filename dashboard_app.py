# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Config

st.set_page_config(
    page_title="Crime Data Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def load_data(file_path):
    """
    Loads the processed crime data from a CSV file.
    Caches the data to improve performance.
    """
    try:
        # file_path = os.path.join(os.getcwd(), file_path)
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"File not found: {file_path}. Please make sure it's in the same directory.")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        st.stop()


DATA_FILE = "enhanced_crime_data.csv"

df = load_data(DATA_FILE)


# Transforming Data

def create_super_motive_category(motive):
    """
    Maps the detailed 'motive_category' to a broader, more generalized category.
    This function implements the logic you requested.
    """
    if pd.isna(motive):
        return "Not Specified"

    motive = motive.lower()

    if 'sexual' in motive:
        return 'Sexual Motives'
    elif 'financial' in motive or 'dowry' in motive or 'property' in motive:
        return 'Financial Motives'
    elif 'relationship' in motive or 'personal_vendetta' in motive:
        return 'Relationship Motives'
    elif 'communal' in motive or 'caste' in motive or 'superstition' in motive:
        return 'Social/Cultural Motives'
    elif 'mental_illness' in motive or 'impulsive' in motive:
        return 'Psychological Motives'
    elif 'political' in motive or 'national_safety' in motive:
        return 'Political Motives'
    elif 'custodial' in motive or 'gang_related' in motive or 'civil_crimes' in motive or 'karnataka_crimes' in motive:
        return 'System-Related'
    else:
        return 'Other Motives'


if 'motive_category' in df.columns:
    df['super_motive_category'] = df['motive_category'].apply(create_super_motive_category)

month_order = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]
if 'month' in df.columns:
    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

# App Layout

# Title and description
st.title("Crime Motives Dashboard")
st.markdown("### Analyzing Crime Distribution by Motive Category")

st.sidebar.header("Filter by Category")

# Super Motive Category filter
if 'super_motive_category' in df.columns:
    selected_super_motives = st.sidebar.multiselect(
        "Select General Motive:",
        options=df['super_motive_category'].unique(),
        default=df['super_motive_category'].unique()
    )
    # Filter the dataframe based on the super motive selection
    filtered_df = df[df['super_motive_category'].isin(selected_super_motives)]
else:
    filtered_df = df.copy()

# Specific Motive Category filter (dependent on the general motive filter)
if 'motive_category' in df.columns:
    selected_motives = st.sidebar.multiselect(
        "Select Specific Motive:",
        options=filtered_df['motive_category'].unique(),
        default=filtered_df['motive_category'].unique()
    )
    filtered_df = filtered_df[filtered_df['motive_category'].isin(selected_motives)]

# Add new filters for major_head and heads_of_crime
if 'major_head' in df.columns:
    selected_major_heads = st.sidebar.multiselect(
        "Select Major Head:",
        options=filtered_df['major_head'].unique(),
        default=filtered_df['major_head'].unique()
    )
    filtered_df = filtered_df[filtered_df['major_head'].isin(selected_major_heads)]

if 'heads_of_crime' in df.columns:
    selected_heads_of_crime = st.sidebar.multiselect(
        "Select Heads of Crime:",
        options=filtered_df['heads_of_crime'].unique(),
        default=filtered_df['heads_of_crime'].unique()
    )
    filtered_df = filtered_df[filtered_df['heads_of_crime'].isin(selected_heads_of_crime)]

# Month filter
if 'month' in df.columns:
    selected_months = st.sidebar.multiselect(
        "Select Month:",
        options=df['month'].cat.categories.tolist(),
        default=df['month'].cat.categories.tolist()
    )
    final_df = filtered_df[filtered_df['month'].isin(selected_months)]
else:
    final_df = filtered_df.copy()

# Main Content

if final_df.empty:
    st.warning("No data found for the selected filters. Please adjust your selections.")
else:
    # Key Metrics
    st.header("Key Statistics")

    total_crimes = len(final_df)
    unique_major_heads = final_df['major_head'].nunique()
    unique_minor_heads = final_df['minor_head'].nunique()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Crimes", value=f"{total_crimes:,}")
    with col2:
        st.metric(label="Unique Major Heads", value=unique_major_heads)
    with col3:
        st.metric(label="Unique Minor Heads", value=unique_minor_heads)

    st.markdown("---")

# Charts
    st.header("Crime Distribution")

    # Chart 1: Distribution by Super Motive Category
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribution by General Motive")
        super_motive_counts = final_df['super_motive_category'].value_counts().reset_index()
        super_motive_counts.columns = ['Super Motive', 'Count']
        fig1 = px.bar(
            super_motive_counts,
            x='Count',
            y='Super Motive',
            orientation='h',
            title='Crimes per General Motive',
            labels={'Super Motive': 'General Motive'},
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        fig1.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig1, use_container_width=True)

    # Chart 2: Distribution by Specific Motive within General Categories
        # Chart 2: Distribution by Specific Motive
        with col2:
            st.subheader("Distribution by Specific Motive")

            # Add a radio button to choose chart type
            chart_type = st.radio(
                "Select chart type:",
                ('Pie Chart', 'Bar Chart'),
                key='motive_chart_type'
            )

            motive_counts = final_df['motive_category'].value_counts().reset_index()
            motive_counts.columns = ['Motive', 'Count']

            if chart_type == 'Pie Chart':
                fig2 = px.pie(
                    motive_counts,
                    values='Count',
                    names='Motive',
                    title='Crimes per Specific Motive',
                    hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
            else:  # Bar Chart
                fig2 = px.bar(
                    motive_counts,
                    x='Count',
                    y='Motive',
                    orientation='h',
                    title='Crimes per Specific Motive',
                    labels={'Motive': 'Specific Motive'},
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig2.update_layout(yaxis={'categoryorder': 'total ascending'})

            st.plotly_chart(fig2, use_container_width=True)

    # Time Series Chart
    st.markdown("---")
    st.header("Monthly Trends")
    monthly_counts = final_df['month'].value_counts().reset_index()
    monthly_counts.columns = ['Month', 'Count']
    monthly_counts = monthly_counts.sort_values('Month')

    fig3 = px.line(
        monthly_counts,
        x='Month',
        y='Count',
        title='Crime Distribution by Month',
        markers=True,
        labels={'Count': 'Number of Crimes'}
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Raw data
    st.markdown("---")
    st.header("Raw Data")
    st.write(final_df)
