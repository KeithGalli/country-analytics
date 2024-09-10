import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from collections import OrderedDict

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
    fig, ax = plt.subplots(figsize=(9, 3))  # 2:1 aspect ratio
    
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

    # Create the line graph
    plt.plot(filtered_df.index, filtered_df['TPopulation1July'], color=color, linewidth=2.5)
    # plt.ylabel('Population')
    # plt.title('Population Over Time')
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

def plot_ages(country_code, color='blue'):
    # Read CSV file
    df = pd.read_csv('./data/worldbank-country-profile.csv', delimiter=';', thousands=',')
    
    # Filter for the specific country
    df = df[df['Country Code'] == country_code]
    
    # Define the indicators we're interested in and their simplified labels, in the desired order
    age_indicators = OrderedDict([
        ('Population ages 0-14 (% of total population)', '0-14'),
        ('Population ages 15-64 (% of total population)', '15-64'),
        ('Population ages 65 and above (% of total population)', '65+')
    ])
    
    # Filter for these indicators
    df_ages = df[df['Indicator Name'].isin(age_indicators.keys())]
    
    # Get the most recent year with data for all indicators
    most_recent_year = df_ages.groupby('Year').count()['Indicator Name'].idxmin()
    
    # Filter for the most recent year and create a series with indicator names as index
    age_data = df_ages[df_ages['Year'] == most_recent_year].set_index('Indicator Name')['Value']
    
    # Convert data to numeric, replacing any non-numeric values with NaN
    age_data = pd.to_numeric(age_data, errors='coerce')
    
    # Reorder the data according to our ordered dictionary
    age_data = age_data.reindex(age_indicators.keys())
    
    # Create the bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(age_indicators.values(), age_data.values, color=color)
    
    # Customize the chart
    plt.title(f'Age Distribution Overview - {country_code} ({most_recent_year})', fontsize=16)
    plt.xlabel('Age Group', fontsize=12)
    plt.ylabel('Percentage of Total Population', fontsize=12)
    plt.ylim(0, 100)  # Set y-axis to go from 0 to 100%
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.1f}%',
                 ha='center', va='bottom')
    
    # Adjust layout and display the chart
    plt.tight_layout()
    plt.show()

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
    image = Image.new('RGB', (1100, 400), color = (255, 255, 255))

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
    most_recent_year = country[country['TPopulation1July'].notnull()].index.max()

    # Get the population for the most recent year
    most_recent_population = country.loc[most_recent_year, 'TPopulation1July']

    return most_recent_population

def get_total_population(country_code, directory='./data'):
    df = pd.read_csv(f'{directory}/country_demographic_data.csv', low_memory=False)
    country = df[df['ISO3_code']==country_code]
    country.set_index('Time', inplace=True)
    columns = ['TPopulation1July']

    # Get the most recent year
    most_recent_year = country.index.max()

    # Get the population for the most recent year
    most_recent_population = country.loc[most_recent_year, 'TPopulation1July']

    return most_recent_population