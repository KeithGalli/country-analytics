import pandas as pd
import subprocess
import os

from colorthief import ColorThief

def rgb_to_hex(r,g,b):
    return '{:02x}{:02x}{:02x}'.format(r, g, b)

codes = pd.read_csv('./data/country-codes.csv', encoding='ISO-8859-1')

for index, row in codes.iterrows():
    iso3 = row['3 Alpha (ISO 3166-2)']
    iso2 = row['2 Alpha (ISO 3166-2)']
    
    default_color = 'blue'
    
    try:
        color_thief = ColorThief(f'./flags/{iso2.lower()}.png')

        r, g, b = color_thief.get_color(quality=2)
        hex_color = rgb_to_hex(r,g,b)
        if not hex_color:
            hex_color = default_color
    except Exception:
        hex_color = default_color

    command = [
        'quarto', 'render', 'country_report.qmd',
        '-P', f'country_code:{iso3}',
        '-P', f"color='#{hex_color}'",
        '-M', f'country_code:{iso3}',
        '-M', f'color:{hex_color}',
        '--output', f'{iso3}.pdf',
    ]

    try: 
        print("Running Command", ' '.join(command))
        result = subprocess.run(command, check=True)

    except Exception as e:
        print(f"Error generating report for {iso3}")
        print(e)