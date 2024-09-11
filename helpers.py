import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from collections import OrderedDict
from datetime import datetime
import re

def plot_country(country_code, zoom_factor=1.1, color='blue'):
    # Load the world map dataset
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    
    # Convert country_code to uppercase
    country_code = country_code.upper()
    
    # Check if it's a 3-letter code or 2-letter code
    if len(country_code) == 3:
        country = world[world['iso_a3'] == country_code]
    else:
        raise ValueError("Invalid country code. Please use a 3 letter code.")
    
    if country.empty:
        raise ValueError(f"No country found with the code {country_code}")
    
    # Create a figure with the desired aspect ratio
    fig, ax = plt.subplots(figsize=(8.7, 2.9))  # 3:1 aspect ratio
    
    # Plot the entire world in light gray
    world.plot(ax=ax, color='white', edgecolor=color)
    
    # Plot the selected country
    country.plot(ax=ax, color=lighten_color(color), edgecolor=color)
    
    # Get the bounding box of the country
    minx, miny, maxx, maxy = country.total_bounds
    
    # Calculate the center of the bounding box
    center_x = (minx + maxx) / 2
    center_y = (miny + maxy) / 2
    
    # Calculate the width and height of the bounding box
    width = maxx - minx
    height = maxy - miny
    
    # Calculate the aspect ratio of the bounding box
    bbox_aspect_ratio = width / height
    
    # Calculate the new width and height to maintain 5:3 aspect ratio
    if bbox_aspect_ratio > 3:
        new_width = width * zoom_factor
        new_height = new_width * (1/3)
    else:
        new_height = height * zoom_factor
        new_width = new_height * (3)
    
    # Set the new limits
    ax.set_xlim(center_x - new_width/2, center_x + new_width/2)
    ax.set_ylim(center_y - new_height/2, center_y + new_height/2)
    
    # Remove axis
    ax.axis('off')
    
    # Adjust the plot to fill the figure
    plt.tight_layout(pad=0)
    
    # Show the plot
    plt.show()

def population_over_time(country_code, directory='./data', color='blue'):

    # plt.style.use('fivethirtyeight')

    df = pd.read_csv(f'{directory}/country_demographic_data.csv', low_memory=False)
    country = df[df['ISO3_code']==country_code]
    country.set_index('Time', inplace=True)
    columns = ['TPopulation1July', 'NetMigrations', 'PopSexRatio', 'MedianAgePop']
    country.head()
    country = country[columns]

    # Filter the data for the desired years
    years = range(1950, 2021, 1)
    filtered_df = country.loc[years]

    upcoming_df = country.loc[[2020,2030]]

    # Create the line graph
    # Divide Y values by 1000 if any one of the values exceeds 1,000,000
    if filtered_df['TPopulation1July'].max() > 1000:
        filtered_df['TPopulation1July'] /= 1000
        upcoming_df['TPopulation1July'] /= 1000
    
    plt.plot(filtered_df.index, filtered_df['TPopulation1July'], color=color, linewidth=2.5)

    # Plot the upcoming years with dashed line
    plt.plot(upcoming_df.index, upcoming_df['TPopulation1July'], color=color, linewidth=2.5, linestyle='--')

    plt.show()

def gender_ratio(country_code, directory='./data/', color='blue'):
    df = pd.read_csv(f'{directory}/country_demographic_data.csv', low_memory=False)
    country = df[df['ISO3_code']==country_code]
    country.set_index('Time', inplace=True)
    columns = ['TPopulation1July', 'NetMigrations', 'PopSexRatio', 'MedianAgePop']

    # Filter the data for the most recent year
    most_recent_year = 2020
    most_recent_data = country.loc[most_recent_year]

    # Create the pie chart
    labels = ['Male', 'Female']

    sizes = [most_recent_data['PopSexRatio']/(most_recent_data['PopSexRatio']+100), 100/(100+most_recent_data['PopSexRatio'])]
    colors = [color, lighten_color(color)]
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
    # plt.title('Gender Ratio')
    plt.show()

def plot_ages_new(country_code, color='blue'):
    df = pd.read_csv('./data/worldbank-country-profile.csv', delimiter=';',)
    YEAR = 2022
    
    # Filter for the specific country
    df = df[(df['Country Code'] == country_code) & (df['Year'] == YEAR)]
    
    # Filter for these indicators
    df = df[df['Indicator Code'].str.startswith('SP.POP') & df['Indicator Code'].str.endswith('5Y')].sort_values(['Indicator Code'])

    # Step 1: Create a base indicator code by removing gender suffix (.FE or .MA)
    df['Base Indicator Code'] = df['Indicator Code'].str.replace(r'\.FE|\.MA', '', regex=True)

    # Step 2: Group by base indicator code and average male/female values
    df_avg = df.groupby(['Country Name', 'Country Code', 'Year', 'Base Indicator Code']).agg({'Value': 'mean'}).reset_index()

    # Step 3: Extract the first two digits of the age group (first two digits in the code represent the group)
    df_avg['Age Group Start'] = df_avg['Base Indicator Code'].str.extract(r'(\d{2})').astype(int)

    # Step 4: Define function to combine specific age groups
    def combine_age_groups(age):
        if age in [0, 5]:  # Combine 00-04 with 05-09
            return '00-09'
        elif age in [10, 15]:  # Combine 10-14 with 15-19
            return '10-19'
        elif age in [20, 25]:  # Combine 20-24 with 25-29
            return '20-29'
        elif age in [30, 35]:  # Combine 30-34 with 35-39
            return '30-39'
        elif age in [40, 45]:  # Combine 40-44 with 45-49
            return '40-49'
        elif age in [50, 55]:  # Combine 50-54 with 55-59
            return '50-59'
        elif age in [60, 65]:  # Combine 60-64 with 65-69
            return '60-69'
        elif age in [70, 75]:  # Combine 70-74 with 75-79
            return '70-79'
        elif age in [80]:
            return '80+'

        return None

    # Step 5: Apply the function to combine age groups
    df_avg['Combined Group'] = df_avg['Age Group Start'].apply(combine_age_groups)

    # Step 6: Group by combined age groups and sum the values
    df_summed = df_avg.groupby(['Country Name', 'Country Code', 'Year', 'Combined Group']).agg({'Value': 'sum'}).reset_index()

    plt.bar(df_summed['Combined Group'], df_summed['Value'], color=color)
    plt.tight_layout()
    plt.show()

    # return df_summed

def lighten_color(hex_color, factor=0.5):
    # Convert hex color to RGB
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # Increase each RGB component to lighten the color
    lighter_rgb = tuple(min(int(c + (255 - c) * factor), 255) for c in rgb)

    # Convert the RGB back to hex
    return '#{:02x}{:02x}{:02x}'.format(*lighter_rgb)

def highlight_text(text, header=None, color='blue'):
    # Create a blank image
    image = Image.new('RGB', (1150, 400), color = (255, 255, 255))

    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)

    # Load a font
    font = ImageFont.truetype("./fonts/OpenSans-Regular.ttf", 150)  # You can specify a custom font path here
    font_small = ImageFont.truetype("./fonts/OpenSans-Regular.ttf", 50)  # You can specify a custom font path here

    # Add text with the font
    draw.text((50, 50), header, font=font_small, fill='gray')
    draw.text((50, 90), text, font=font, fill=color)

    # Show the image
    display(image)

def get_total_population(country_code, directory='./data'):
    df = pd.read_csv(f'{directory}/country_demographic_data.csv', low_memory=False)
    country = df[df['ISO3_code']==country_code]
    country.set_index('Time', inplace=True)
    columns = ['TPopulation1July']

    # Get the most recent year where TPopulation1July is not None
    
    most_recent_year = datetime.now().year

    # Get the population for the most recent year
    most_recent_population = country.loc[most_recent_year, 'TPopulation1July']

    return most_recent_population*1000

def get_median_age(country_code, directory='./data'):
    df = pd.read_csv(f'{directory}/country_demographic_data.csv', low_memory=False)
    country = df[df['ISO3_code']==country_code]
    country.set_index('Time', inplace=True)
    columns = ['MedianAgePop']

    most_recent_year = datetime.now().year

    # Get the population for the most recent year
    median_age = country.loc[most_recent_year, 'MedianAgePop']

    return median_age

def get_life_expectancy(country_code, directory='./data'):
    df = pd.read_csv(f'{directory}/country_demographic_data.csv', low_memory=False)
    country = df[df['ISO3_code']==country_code]
    country.set_index('Time', inplace=True)
    columns = ['LEx']

    # Filter the data for the most recent year
    most_recent_year = datetime.now().year
    most_recent_data = country.loc[most_recent_year]

    # Get the life expectancy for the most recent year
    life_expectancy = most_recent_data['LEx']

    return life_expectancy