import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def x(database):
    pd.set_option('display.max_columns', None)
    df = pd.read_sql_query("SELECT * FROM features_data", database)
    print(df.head(10))
    print(df.info())

# danceability vs speechiness
def speechiness_vs_danceability(database):
    df = pd.read_sql_query("SELECT danceability, speechiness FROM features_data", database)

    correlation = df["speechiness"].corr(df["danceability"])
    print("The correlation between speechiness and danceability is: %.4f" % correlation)

    df.plot.scatter(x="speechiness", y="danceability", s=5, alpha=0.1)
    plt.xlabel("Speechiness")
    plt.ylabel("Danceability")
    plt.title("Comparison speechiness and danceability")
    plt.show()

def comparison_two_features(database, feature1, feature2):
    df = pd.read_sql_query(f"""SELECT {feature1}, {feature2} FROM features_data""", database)

    correlation = df[feature1].corr(df[feature2])
    print(f"The correlation between {feature1} and {feature2} is: %.4f" % correlation)

    df.plot.scatter(x=f"{feature1}", y=f"{feature2}", s=5, alpha=0.1)
    plt.xlabel(f"{feature1}")
    plt.ylabel(f"{feature2}")
    plt.title(f"Comparison {feature1} and {feature2}")
    plt.show()

# danceability vs energy vs tempo
def danceability_vs_energy_vs_tempo(database):
    df = pd.read_sql_query("SELECT danceability, energy, tempo FROM features_data", database)

    corr_de = df["danceability"].corr(df["energy"])
    corr_dt = df["danceability"].corr(df["tempo"])
    corr_et = df["energy"].corr(df["tempo"])

    print("Correlation between danceability and energy: %.4f" % corr_de)
    print("Correlation between danceability and tempo: %.4f" % corr_dt)
    print("Correlation between energy and tempo: %.4f" % corr_et)

    pp = sns.pairplot(df, diag_kind='kde', plot_kws={'s': 5, 'alpha': 0.1})
    pp.fig.suptitle(f"Comparison danceability, energy, tempo", fontsize=16)
    pp.fig.subplots_adjust(top=0.95)
    plt.show()

# speechiness (spoken words) vs acousticness vs instrumentalness (no vocals)
def acousticness_vs_instrumentalness_vs_speechiness(database):
    df = pd.read_sql_query("SELECT acousticness, instrumentalness, speechiness FROM features_data", database)

    corr_ai = df["acousticness"].corr(df["instrumentalness"])
    corr_as = df["acousticness"].corr(df["speechiness"])
    corr_is = df["instrumentalness"].corr(df["speechiness"])

    print("Correlation between acousticness and instrumentalness: %.4f" % corr_ai)
    print("Correlation between acousticness and speechiness: %.4f" % corr_as)
    print("Correlation between instrumentalness and speechiness: %.4f" % corr_is)

    pp = sns.pairplot(df, diag_kind='kde', plot_kws={'s': 5, 'alpha': 0.1})
    pp.fig.suptitle(f"Comparison acousticness, instrumentalness, speechiness", fontsize=16)
    pp.fig.subplots_adjust(top=0.95)
    plt.show()

def comparison_three_features(database, feature1, feature2, feature3):
    df = pd.read_sql_query(f"""SELECT {feature1}, {feature2}, {feature3} FROM features_data""", database)

    corr_one_two = df[feature1].corr(df[feature2])
    corr_one_three = df[feature1].corr(df[feature3])
    corr_two_three = df[feature2].corr(df[feature3])

    print(f"Correlation between {feature1} and {feature2}: %.4f" % corr_one_two)
    print(f"Correlation between {feature1} and {feature3}: %.4f" % corr_one_three)
    print(f"Correlation between {feature2} and {feature3}: %.4f" % corr_two_three)

    pp = sns.pairplot(df, diag_kind='kde', plot_kws={'s': 5, 'alpha': 0.1})
    pp.fig.suptitle(f"Comparison {feature1}, {feature2}, {feature3}", fontsize=16)
    pp.fig.subplots_adjust(top=0.95)
    plt.show()

def outliers(database):
    df = pd.read_sql("SELECT * FROM features_data", database)
    features = [
        'danceability', 'energy', 'loudness', 'speechiness',
        'acousticness', 'instrumentalness', 'liveness',
        'valence', 'tempo', 'duration_ms'
    ]
    outlier_counts = {}
    for col in features:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower) | (df[col] > upper)]
        outlier_counts[col] = len(outliers)

    plt.figure(figsize=(15, 10))
    for i, col in enumerate(features):
        plt.subplot(4, 3, i + 1)
        sns.boxplot(x=df[col])
        plt.title(col)
    plt.tight_layout()
    plt.show()