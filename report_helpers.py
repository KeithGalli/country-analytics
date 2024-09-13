import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

AGE_GROUP_MAP = {
    (0, 5): '00-09',
    (10, 15): '10-19',
    (20, 25): '20-29',
    (30, 35): '30-39',
    (40, 45): '40-49',
    (50, 55): '50-59',
    (60, 65): '60-69',
    (70, 75): '70-79',
    (80, 80): '80+'
}

def plot_country(country_code, zoom_factor=1.1, color='blue'):  
    file = './map/ne_110m_admin_0_countries.shp'
    world = gpd.read_file(file)

    country_code = country_code.upper()
    
    if len(country_code) == 3:
        country = world[world['ISO_A3'] == country_code]
    else:
        raise ValueError("Invalid country code. Please use a 3 letter code.")
    
    if country.empty:
        raise ValueError(f"No country found with the code {country_code}")
    
    fig, ax = plt.subplots(figsize=(8.7, 2.9))
    world.plot(ax=ax, color='white', edgecolor=color)
    country.plot(ax=ax, color=lighten_color(color), edgecolor=color)
    
    minx, miny, maxx, maxy = country.total_bounds
    center_x = (minx + maxx) / 2
    center_y = (miny + maxy) / 2
    width = maxx - minx
    height = maxy - miny
    bbox_aspect_ratio = width / height
    
    if bbox_aspect_ratio > 3:
        new_width = width * zoom_factor
        new_height = new_width * (1/3)
    else:
        new_height = height * zoom_factor
        new_width = new_height * (3)
    
    ax.set_xlim(center_x - new_width/2, center_x + new_width/2)
    ax.set_ylim(center_y - new_height/2, center_y + new_height/2)
    ax.axis('off')
    
    plt.tight_layout(pad=0)
    plt.show()

def population_over_time(df, year=2023, color='blue'):
    columns = ['TPopulation1July']
    df = df[columns]

    # Historical data (up to the current year)
    historical_df = df.loc[range(1950, year)]

    # Forecasted data (from the current year onwards)
    forecast_df = df.loc[range(year, year + 10)]

    # Check if the population exceeds 1 million people
    max_population = historical_df['TPopulation1July'].max()

    if max_population >= 1000:
        # If population is over 1 million, plot in millions
        historical_df['TPopulation1July'] /= 1000
        forecast_df['TPopulation1July'] /= 1000
        y_label = "Population (Millions)"
    else:
        # Otherwise, plot in thousands
        y_label = "Population (Thousands)"

    # Plot historical data
    plt.plot(historical_df.index, historical_df['TPopulation1July'], color=color, linewidth=2.5)
    
    # Plot forecasted data with a dashed line
    plt.plot(forecast_df.index, forecast_df['TPopulation1July'], color=color, linewidth=2.5, linestyle='--')

    plt.ylabel(y_label)
    plt.tight_layout()
    plt.show()

def gender_ratio(df, year=2023, color='blue'):
    most_recent_data = df.loc[year]

    labels = ['Male', 'Female']
    sizes = [most_recent_data['PopSexRatio']/(most_recent_data['PopSexRatio']+100), 
             100/(100+most_recent_data['PopSexRatio'])]
    colors = [color, lighten_color(color)]
    
    plt.figure(figsize=(6, 6))
    _, _, autotexts = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', textprops={"fontsize": 18})
    for autotext in autotexts:
        autotext.set_color('white')
    plt.show()

# Note: Use worldbank DF for this function
def plot_ages(df, year=2023, color='blue'):
    df = df[df['Indicator Code'].str.startswith('SP.POP') & df['Indicator Code'].str.endswith('5Y')].sort_values(['Indicator Code'])

    df['Base Indicator Code'] = df['Indicator Code'].str.replace(r'\.FE|\.MA', '', regex=True)
    df_avg = df.groupby(['Country Name', 'Country Code', 'Year', 'Base Indicator Code']).agg({'Value': 'mean'}).reset_index()
    
    df_avg['Age Group Start'] = df_avg['Base Indicator Code'].str.extract(r'(\d{2})').astype(int)
    df_avg['Combined Group'] = df_avg['Age Group Start'].apply(combine_age_groups)

    df_summed = df_avg.groupby(['Country Name', 'Country Code', 'Year', 'Combined Group']).agg({'Value': 'sum'}).reset_index()

    plt.bar(df_summed['Combined Group'], df_summed['Value'], color=color)
    plt.ylabel("% of Population")
    plt.tight_layout()
    plt.show()

def combine_age_groups(age):
    for (start, end), group in AGE_GROUP_MAP.items():
        if age in range(start, end+1):
            return group
    return None

def lighten_color(hex_color, factor=0.5):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    lighter_rgb = tuple(min(int(c + (255 - c) * factor), 255) for c in rgb)
    return '#{:02x}{:02x}{:02x}'.format(*lighter_rgb)

def highlight_text(text, header=None, color='blue'):
    image = Image.new('RGB', (1150, 400), color = (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("./fonts/OpenSans-Regular.ttf", 150)
    font_small = ImageFont.truetype("./fonts/OpenSans-Regular.ttf", 50)

    draw.text((50, 50), header, font=font_small, fill='gray')
    draw.text((50, 90), text, font=font, fill=color)

    display(image)

def get_country_stat(df, column_name, year=2023):
    return df.loc[year, column_name]