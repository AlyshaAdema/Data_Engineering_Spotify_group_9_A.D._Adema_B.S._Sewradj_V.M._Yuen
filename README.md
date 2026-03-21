# Data Engineering Spotify group 9

This project analyzes Spotify artist and music data using multiple datasets, which are stored in a database. The datasets include:
- **Artist dataset**
- **Albums dataset**
- **Features dataset**
- **Tracks dataset**

Each dataset is analyzed to explore relationships between music characteristics, popularity, artist statistics, and other relevant metrics. The analyses are organized across multiple files in this repository.

### Repository Contents
- **Analysis files** - Scripts for calculating statistics and exploring the data
- **Visualization files** - Scripts for creating charts and graphs of the data
- **Final dashboard file** - The main dashboard visualizing insights.
- **Dashboard requirements** - List of tools and packages needed to run the dashboard
- **.streamlit folder** - Custom configuration for the dashboard's styling
- **Database** - The Spotify database used for analysis

Most files and folders in this repository are self-explanatory. This section focuses on the **analysis** and **visualization** files.

## Analysis and Visualization Files

There are four main topics analyzed in the repository, each represented by an analysis file and a corresponding visualization file:
- **Albums_data**
- **Artist_data**
- **Features_data**
- **Full_database**

In total, there are eight files: each topic has one analysis file and one visualization file.

### How the files are organized
The **analysis files** calculate statistics, correlations, and other insights for a specific dataset. For example, 'Albums_data_analysis' studies the albums dataset, examining patterns such as the number of albums, number of tracks per album, and relationships between these features.
The **visualization files** create charts and graphs based on the calculations from the corresponding analysis file.

### Specific dataset notes
'Artist_data' and 'Features_data' follow the same structure as 'Albums_data', but focus on the artist and features datasets, respectively.
There are no seperate analysis or visualization files for the tracks dataset, because it is small and required less in-depth exploration. However, the tracks data is included in the **Full_database** files.
The **Full_database** analysis connects all the datasets and generates insights from combined information. Its visualization file shows charts and graphs based on these combined analyses, including data from the tracks dataset.

## Conclusion
This repository provides tools and analyses to explore Spotify music and artist data. The dashboard presents key insights in an interactive way. Users can run the analysis and visualization scripts to explore the data further or use the dashboard to quickly view results.
