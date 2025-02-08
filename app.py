import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_data.csv")
    df.dropna(inplace=True)
    df['date_added'] = pd.to_datetime(df['date_added'])
    return df

df = load_data()

# sidebar filters
st.sidebar.header("Filters")
content_type = st.sidebar.multiselect("Select Content Type", df["type"].unique(), default=df["type"].unique())
countries = st.sidebar.multiselect("Select Country", df["country"].unique(), default=df["country"].unique()[:10])
year_range = st.sidebar.slider("Select Release Year Range", int(df["release_year"].min()), int(df["release_year"].max()), (2000, 2022))

# filter data
filtered_df = df[(df["type"].isin(content_type)) & (df["country"].isin(countries)) & (df["release_year"].between(year_range[0], year_range[1]))]

st.title("📊 Netflix EDA & Visualization Dashboard")
st.markdown("---")

st.write("### Data Preview")
st.dataframe(filtered_df)

# content distribution 
st.subheader("Distribution of Movies and TV Shows")
fig1 = px.pie(filtered_df, names='type', title='Content Type Distribution', hole=0.3)
st.plotly_chart(fig1)

# top 10 directors
st.subheader("Top 10 Directors with Most Content")
top_directors = df['director'].dropna().value_counts().head(10)
fig2, ax = plt.subplots()
sns.barplot(x=top_directors.values, y=top_directors.index, hue=top_directors.index, palette='coolwarm', legend=False, ax=ax)
ax.set_xlabel("Number of Titles")
st.pyplot(fig2)

# content added Over the months and years
st.subheader("Trend of Content Added Over Time by Type")
df_yearly = df.groupby([df['date_added'].dt.year, 'type']).size().reset_index(name='count')
fig3 = px.line(df_yearly, x='date_added', y='count', color='type', title='Content Added Over the Years')
st.plotly_chart(fig3)

# monthly releases trend
st.subheader("Trend of Content Added by Month")
df_monthly = df.groupby(df['date_added'].dt.to_period('M')).size().reset_index(name='count')
df_monthly['date_added'] = df_monthly['date_added'].astype(str)
fig4 = px.line(df_monthly, x='date_added', y='count', title='Monthly Content Additions')
st.plotly_chart(fig4)

# content by country
st.subheader("Top 10 Countries Producing Netflix Content")
top_countries = df['country'].value_counts().head(10)
fig5, ax = plt.subplots()
sns.barplot(y=top_countries.index, x=top_countries.values, hue=top_countries.index, palette='viridis', legend=False, ax=ax)
st.pyplot(fig5)

# rating distribution
st.subheader("Content Rating Distribution")
fig6 = px.histogram(filtered_df, x='rating', title='Rating Distribution', color='rating')
st.plotly_chart(fig6)

# duration analysis
st.subheader("Distribution of Content Duration")
df['duration'] = df['duration'].str.extract(r'(\d+)').astype(float)
fig7, ax = plt.subplots()
sns.histplot(df[df['type'] == 'Movie']['duration'], bins=20, kde=True, color='blue', ax=ax)
ax.set_title("Movie Duration Distribution")
st.pyplot(fig7)

# genre distribution
st.subheader("Most Common Genres on Netflix")
genre_counts = df['listed_in'].str.split(', ').explode().value_counts().head(15)
fig8, ax = plt.subplots()
sns.barplot(x=genre_counts.values, y=genre_counts.index, hue=genre_counts.index, palette='magma', legend=False, ax=ax)
st.pyplot(fig8)

st.markdown(
    """
    <hr>
    <div style='text-align: center;'>
        <p style='font-size: 1.2em; font-family: "Arial", sans-serif;'>
            © 2025 All rights reserved by <a href='https://github.com/Ironsoldier353' target='_blank'><img src='https://img.icons8.com/?size=100&id=LoL4bFzqmAa0&format=png&color=000000' height='30' style='vertical-align: middle;'></a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)