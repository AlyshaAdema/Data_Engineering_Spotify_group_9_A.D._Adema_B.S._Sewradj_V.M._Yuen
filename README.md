# Data Engineering Spotify group 9
This project analyzes Spotify artist and music data.

The project uses multple datasets that are put together in a database. These datasets include:
- Artist dataset
- Albums dataset
- Features dataset
- Tracks dataset

Each dataset is analyzed to explore relationships between music characteristics, popularity, artist statistics and a lot more. These analyses are done in mutliple files in this repository. A quick summary of files that are in the repository are:
- The analysis files
- The final dashboard file
- The requirements for the dashboard
- .streamlit that changes the style of the dashboard
- The database

## Artist DataSet Analysis
The artist dataset contains information about Spotify artists and their musical profiles. The dataset includes the following attributes:
- Artist name
- Number of followers
- Popularity score (ranges from 0 to 100)
- Associated musical genres

### Analysis Performed
Several statistical analyses were performed to explore relationships between variables, identify patterns, and detect notable observations with the dataset.

The analysis focused on:
- Correlations between variables such as followers and popularity
- Detection of outliers using regression residuals
- Identification of top-performing artists and genres
 
These analyses are implemented in the file artist_data_analysis.py, which contains functions responsible for statistical computation and data processing.

To improve interpretability of results, a separate file artist_data_visualization.py was created. This file contains functions used to generate visual representations of the dataset, making trends and relationships easier to interpret.

