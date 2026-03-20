# Data Engineering Spotify group 9
This project analyzes Spotify artist and music data.

The project uses multple datasets including:
- artist dataset
- volgende datasets wanneer we die gebruikt hebben

Each dataset is analyzed to explore relationships between music characteristics, popularity, and artist statistics. (dit miss nog aanpassen als we ook andere dingen gaan onderzoeken want weet nog niet wat de andere datasets zijn :))

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

