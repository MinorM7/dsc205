#Imports
import streamlit as st
from matplotlib.dates import DateFormatter
import datetime
from geopy.geocoders import Nominatim
import pycountry
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression


#Functions
# For map
def get_coordinates(country):
    try:
        country_obj = pycountry.countries.get(name=country)
        geolocator = Nominatim(user_agent="my-application")
        location = geolocator.geocode(country_obj.name)
        return location.latitude, location.longitude
    except AttributeError:
        return None, None
# Prevents loading the file every time the user interacts with widgets
def load_data(selected_year):
    URL = 'https://raw.githubusercontent.com/MinorM7/dsc205/main/CountryHappinessRank{}.csv'.format(selected_year)
    df = pd.read_csv(URL)
    return df


# Load datasets
df1  = pd.read_csv("https://raw.githubusercontent.com/MinorM7/dsc205/main/CountryHappinessRank2015.csv")
df2  = pd.read_csv("https://raw.githubusercontent.com/MinorM7/dsc205/main/CountryHappinessRank2016.csv")
df3  = pd.read_csv("https://raw.githubusercontent.com/MinorM7/dsc205/main/CountryHappinessRank2017.csv")
df4  = pd.read_csv("https://raw.githubusercontent.com/MinorM7/dsc205/main/CountryHappinessRank2018.csv")
df5  = pd.read_csv("https://raw.githubusercontent.com/MinorM7/dsc205/main/CountryHappinessRank2019.csv")
year_to_df = {
    2015: df1,
    2016: df2,
    2017: df3,
    2018: df4,
    2019: df5
}


# TITLE
st.title('😀World Happiness🌍')
st.subheader('by Minor Molina')

# viz1
st.markdown('---')
st.markdown('Dive into the changing landscape of happiness rankings across countries from 2015 to 2019. This dashboard offers a visual journey through annual happiness ranks, allowing you to compare and observe trends in countries well-being.')
st.markdown('---')
st.subheader('Regions and their Highest Score')
selected_year = st.radio('Select a year', [2015,2016])

# Load picked dataset
df = load_data(selected_year)

max_score_country = df.loc[df.groupby('Region')['HappinessScore'].idxmax()]
max_score_country = max_score_country.sort_values('HappinessScore', ascending=True)
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot()
bars = ax.barh( max_score_country['Region'], max_score_country['HappinessScore'])
ax.set_title('Highest Happiness Scores by Region')
ax.set_xlabel('Score')
ax.set_ylabel('Regions')
st.pyplot(fig)

# viz2
st.markdown('---')
st.subheader('Timeseries')
country_name = st.selectbox('Select a Country', df['Country'].unique())
criteria = st.radio('Select GDP or Rank', ['GDP','HappinessRank'])
years = [2015,2016,2017,2018,2019]
fiveyrscores = [df1.loc[df1['Country'] == country_name, criteria].iloc[0], 
                df2.loc[df2['Country'] == country_name, criteria].iloc[0], 
                df3.loc[df3['Country'] == country_name, criteria].iloc[0], 
                df4.loc[df2['Country'] == country_name, criteria].iloc[0], 
                df5.loc[df2['Country'] == country_name, criteria].iloc[0]]

plt.figure(figsize=(8, 6))
plt.scatter(years, fiveyrscores, marker='o')
plt.xlabel('Year')
plt.xticks(years)
if criteria == 'GDP':
    ytixs = [0,.5,1,1.5,2,2.5,3]
elif criteria == 'HappinessRank':
    ytixs = range(0,160,25)
plt.yticks(ytixs) 
plt.ylabel(criteria)
plt.title("{}'s {} from 2015 to 2019".format(country_name,criteria))
st.pyplot(plt)

# viz3
st.markdown('---')
st.subheader('Lets look at correlation of parameters')
st.markdown('We can see what positively correlates with the level of happiness (score) the most:  \n-GDP per capita  \n-Social support  \n-Freedom to make life choices')
fig, ax = plt.subplots()
sns.heatmap(df4.corr(numeric_only=True), annot=True)
st.write(fig)

# viz4
st.markdown('---')
st.subheader('Happiness Score Histogram by Region')
# Dropdown to select a region
selected_region = st.selectbox('Select a Region', df['Region'].unique())
# Filter the DataFrame based on the selected region
region_data = df[df['Region'] == selected_region]
# Create
fig, ax = plt.subplots(figsize=(8, 6))
# Plot the histogram on the Matplotlib axis
ax.hist(region_data['HappinessScore'], bins=10, color='skyblue', edgecolor='black')
# Set labels and title
ax.set_xlabel('Happiness Score')
ax.set_ylabel('Frequency')
ax.set_title(f'Histogram of Happiness Scores in {selected_region}')
# Display the Matplotlib figure using st.pyplot()
st.pyplot(fig)

# viz5
st.markdown('---')
st.subheader('Factors that most affect Happiness Score: Top 10')
selected_yr = st.selectbox('Select a year', [2015,2016,2016,2017,2018,2019])
selected_df = year_to_df[selected_yr]

df_top10_2019 = selected_df.sort_values('HappinessScore', ascending=False).head(10)
factors = df_top10_2019.iloc[:, 3:].columns
num_countries = len(df_top10_2019)
num_factors = len(factors)
factor_values = np.zeros((num_countries, num_factors))

for i, factor in enumerate(factors):
    factor_values[:, i] = df_top10_2019[factor]


plt.figure(figsize=(10, 6))
for i in range(num_factors):
    plt.bar(df_top10_2019['Country'], factor_values[:, i], label=factors[i], bottom=np.sum(factor_values[:, :i], axis=1))

plt.xlabel('Country')
plt.ylabel('Happiness Score')
plt.title('Influence of factors {}'.format(selected_yr))
plt.xticks(rotation=45, ha='right')
plt.legend()
st.pyplot(plt)

# viz6
st.markdown('---')
st.subheader('Factors that most affect Happiness Score: Bottom 10')
df_bot10_2019 = df5.sort_values('HappinessScore', ascending=True).head(10)
factors = df_bot10_2019.iloc[:, 3:].columns
num_countries = len(df_bot10_2019)
num_factors = len(factors)
factor_values = np.zeros((num_countries, num_factors))

for i, factor in enumerate(factors):
    factor_values[:, i] = df_bot10_2019[factor]


plt.figure(figsize=(10, 6))
for i in range(num_factors):
    plt.bar(df_bot10_2019['Country'], factor_values[:, i], label=factors[i], bottom=np.sum(factor_values[:, :i], axis=1))

plt.xlabel('Country')
plt.ylabel('Happiness Score')
plt.title('Influence of factors (2019)')
plt.xticks(rotation=45, ha='right')
plt.legend()
st.pyplot(plt)

# viz7
st.markdown('---')
st.subheader('Map Displaying Highest Scoring Countries per Region')
country_coor_lat = [27.5142, 20.3484, 23.69780, 49.8175, 1.35210, 9.7489 ,31.0461 , 40.9006 , 56.1304, 46.8182]
country_coor_lon = [90.4336, 57.5522, 120.9605, 15.4730,103.8198, 83.7534,34.8516 , 174.8860,106.3468, 8.2275 ]
max_score_country['lat'] = country_coor_lat
max_score_country['lon'] = country_coor_lon 
st.map(max_score_country)
