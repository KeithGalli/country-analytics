import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

def plot_country_location(country_code, zoom=1.5, fig_width=16, fig_height=9):
    # Load the world map shapefile
    world = gpd.read_file("./map")
    
    # Filter for the specific country
    country = world[world.ISO_A3.str.lower() == country_code.lower()]
    if country.empty:
        print(f"Country '{country_code}' not found in world dataset!")
        return
    
    # Create the figure with specified dimensions
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Plot the world boundaries
    world.boundary.plot(ax=ax, linewidth=1, color='#192f5d')
    
    # Plot the specific country
    country.plot(ax=ax, color='#192f5d')
    
    # Get the bounding box of the country
    minx, miny, maxx, maxy = country.total_bounds
    
    # Calculate the center and dimensions of the bounding box
    center_x = (minx + maxx) / 2
    center_y = (miny + maxy) / 2
    bbox_width = maxx - minx
    bbox_height = maxy - miny
    
    # Determine which dimension to base the zoom on
    if bbox_width / fig_width > bbox_height / fig_height:
        # Width is the limiting factor
        ax.set_xlim(center_x - bbox_width/2 * zoom, center_x + bbox_width/2 * zoom)
        y_zoom = (bbox_width * zoom * fig_height) / (bbox_height * fig_width)
        ax.set_ylim(center_y - bbox_height/2 * y_zoom, center_y + bbox_height/2 * y_zoom)
    else:
        # Height is the limiting factor
        ax.set_ylim(center_y - bbox_height/2 * zoom, center_y + bbox_height/2 * zoom)
        x_zoom = (bbox_height * zoom * fig_width) / (bbox_width * fig_height)
        ax.set_xlim(center_x - bbox_width/2 * x_zoom, center_x + bbox_width/2 * x_zoom)
    
    # Remove axis
    ax.axis('off')
    
    plt.tight_layout()
    plt.show()

def plot_country(country_code, zoom_factor=1.1):
    # Load the world map dataset
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    
    # Convert country_code to uppercase
    country_code = country_code.upper()
    
    # Check if it's a 3-letter code or 2-letter code
    if len(country_code) == 3:
        country = world[world['iso_a3'] == country_code]
    elif len(country_code) == 2:
        country = world[world['iso_a2'] == country_code]
    else:
        raise ValueError("Invalid country code. Please use a 2 or 3 letter code.")
    
    if country.empty:
        raise ValueError(f"No country found with the code {country_code}")
    
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the entire world in light gray
    world.plot(ax=ax, color='lightgray', edgecolor='black')
    
    # Plot the selected country in red
    country.plot(ax=ax, color='red', edgecolor='black')
    
    # Get the bounding box of the country
    ZOOM = 20
    minx, miny, maxx, maxy = country.total_bounds
    ax.set_xlim(minx - ZOOM, maxx + ZOOM)
    ax.set_ylim(miny - ZOOM, maxy + ZOOM)
    
    # Remove axis
    ax.axis('off')
    
    # Set the title to the country name
    plt.title(country['name'].values[0])
    
    # Show the plot
    plt.show()

def population_over_time(COUNTRY='japan'):
plt.style.use('fivethirtyeight')

    df = pd.read_csv('./country_demographic_data.csv', low_memory=False)
    country = df[df['Location'].str.lower()==COUNTRY]
    country.set_index('Time', inplace=True)
    columns = ['TPopulation1July', 'NetMigrations', 'PopSexRatio', 'MedianAgePop']
    country.head()
    country = country[columns]

    # Filter the data for the desired years
    years = range(1950, 2021, 1)
    filtered_df = country.loc[years]

    # Create the line graph
    plt.plot(filtered_df.index, filtered_df['TPopulation1July'])
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.title('Population Over Time')
    plt.show()