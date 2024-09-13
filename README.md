# Country Analytics Reports w/ Quarto

![Report](images/report-sample.png)

## Overview

Quarto is an open-source publishing system for websites, dashboards, reports, presentations, and more. In this repository we create country analytics reports using Quarto & Python.

The YouTube video corresponding to this repository can be viewed [here](https://youtu.be/dQw4w9WgXcQ?si=dPBNv-5YEO27OssV).

Feel free to check out samples reports for [USA](./outputs/USA.pdf), [India](./outputs/IND.pdf), & [Argentina](./outputs/ARG.pdf).

## Setup

First, I recommend forking the repo (button in top-right corner). Once you have your own forked copy of the repo, clone it locally using the following command:
```sh
git clone https://github.com/<YOUR USERNAME>/<YOUR REPO>.git
```
*Note: You can also click on the green code button to get your specific URL*

Once you have the repo locally, you'll want to install the necessary libraries using the following terminal commands (*it is good practice to first [activate a virtual environment](https://docs.python.org/3/tutorial/venv.html), but not necessary*)
```sh
cd country-analytics  # Replace this with your name for the repo
pip install -r requirements.txt
```

You then may want to add Quarto extensions to your preferred code editor using [this link](https://quarto.org/docs/get-started/). The Quarto-cli was already installed via pip, so downloading that should not be necessary. If you don't see your preferred editor listed, no problem, you can also generate reports from the command line.

The report is designed in Quarto Markdown (.qmd) by the file [country_report.qmd](./country_report.qmd). You can directly add code and markdown in this file. To keep the .qmd file more organized, most of the graph code is imported from [./report_helpers.py](./report_helpers.py).

To generate a new report, from the root directory of this repo, try running the following command:
```sh
quarto render country_report.qmd
```

If successful you should see a PDF output in the [./outputs/](./outputs/) directory. You can change this directory to one of your choosing by modifying the [_quarto.yml](./_quarto.yml) file.

You can also list out additional render options by doing the following
```sh
quarto render -h
```

### Generate all reports

An additional file called [create_all_reports.py](./create_all_reports.py) shows how you can generate hundreds of country reports automatically. Additionally, it leverages the *[colorthief library](https://github.com/fengsp/color-thief-py)* to obtain a primary country color for each report by looking at that country's flag in the [./flags](./flags) directory.



## Data Sources

### United Nations

To access populations over time, male/female gender ratio, median age, and life expectancy we leverage the [World Populations Prospects Dataset](https://population.un.org/wpp/Download/Standard/CSV/) from the United Nations.

### World Bank

To access age distribution information, we leverage the [World Bank World Development Indicators Database](https://databank.worldbank.org/source/world-development-indicators/preview/on). There are many additional data fields that could be incorporated into a report from this data source, but to keep the file size appropriate for a Github repository, only the age distribution indicators were kept. To easily download a more complete version of the dataset, check out this [Kaggle Dataset](https://www.kaggle.com/datasets/joebeachcapital/world-bank-country-profile).

*Note: this Kaggle source file may be ';' delimited. If you want to load it into Pandas, you'll likely need to do a `pd.read_csv('worldbank-country-profile.csv', delimiter=';')`*

### Country Flags Repository

I found a helpful repo with country-code mappings & png images of each country's flag that I've brought into this repo. The repo I used was created by @csmoore can be [found here](https://github.com/csmoore/country-flag-icons)

## Additional Sources

Special shout-out to David Keyes and the [R for the Rest of Us](https://rfortherestofus.com/) team for the typst templates and lot of other great Quarto insights. I recommend checking out his [recent talk](https://www.youtube.com/@PositPBC) at Posit Conf!

## Next Steps

I would love to see where people take these reports! Please customize & make them your own. For inspiration, here are some ideas that you could try implementing:

1. Incorporate addtional or different data fields into your reports by using the full World Bank & UN data files.

2. Take multiple colors from a country's flag and incorporate the additional color(s) into your report. *Hint: the colorthief library has a get_palette() function that will be helpful for this*

3. Make your reports interactive by rendering them to HTML and using a graphing library like Plotly.

Publish your Quarto Reports by using [Posit Connect Cloud](https://connect.posit.cloud/)

Share published reports with me by tagging me (@KeithGalli) on LinkedIn, X, Instagram, etc. and/or add the hashtag #QuartoCountry
