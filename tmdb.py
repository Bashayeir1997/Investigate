import pandas as pd
import warnings
import numpy as np
import matplotlib.pyplot as plt
warnings.simplefilter(action='ignore', category=FutureWarning)

A=2

# Load the CSV data into a pandas DataFrame
df = pd.read_csv("tmdb-movies.csv")
# Convert the 'release_date' column to datetime type
df['release_date'] = pd.to_datetime(df['release_date']).dt.year
# Get all unique genres
all_genres = set('|'.join(df['genres']).split('|'))
genre_binary = {genre: [] for genre in all_genres}
for genres in df['genres']:
    genre_list = genres.split('|')
    for genre in all_genres:
        genre_binary[genre].append(1 if genre in genre_list else 0)

# Create a new DataFrame with the binary columns
binary_df = pd.DataFrame(genre_binary)
binary_df = pd.concat([df, binary_df], axis=1)

binary_df.to_csv('binary.csv')
#print(binary_df)
print('-' * 40)


genre_counts_by_year = binary_df.groupby('release_year').sum()
genre_per_year = genre_counts_by_year[['Crime','Drama','Western','Romance','History','Science Fiction','War','TV Movie','Foreign','Horror','Mystery','None','Animation','Adventure','Family','Comedy','Thriller','Music','Action','Fantasy','Documentary']]
max_column_for_each_year = genre_counts_by_year[['Crime','Drama','Western','Romance','History','Science Fiction','War','TV Movie','Foreign','Horror','Mystery','None','Animation','Adventure','Family','Comedy','Thriller','Music','Action','Fantasy','Documentary']].idxmax(axis=1)
print('top genre per year')
print(max_column_for_each_year)
print('-' * 40)


def desc_func(df):
# Take the first 20 rows
    top_20 = df[['popularity','budget','revenue','runtime','vote_average','release_year','budget_adj','revenue_adj']].head(20)
    #sum_df = top_20_revenue.sum().astype(int)
    mean_df = (top_20.mean()).astype(int)
    #sum_df = (top_20.sum()).astype(int)
    #print('most genere  movies top 20 characters ')
    print(mean_df)


df_sorted_revenue = binary_df.sort_values(by='revenue', ascending=False)
print('describe top 20 movies revenue without inflation')
desc_func(df_sorted_revenue)
print('-' * 40)

df_sorted_budget = binary_df.sort_values(by='budget', ascending=False)
print('describe top 20 movies budget without inflation')
desc_func(df_sorted_budget)
print('-' * 40)


df_sorted_revenue = binary_df.sort_values(by='revenue_adj', ascending=False)
print('describe top 20 movies revenue with inflation')
desc_func(df_sorted_revenue)
print('-' * 40)

df_sorted_budget = binary_df.sort_values(by='budget_adj', ascending=False)
print('describe top 20 movies revenue with inflation')
desc_func(df_sorted_budget)
print('-' * 40)

top_directors_by_movies = df['director'].str.split('|', expand=True).stack().value_counts()
# Get the total revenue for each director
directors_revenue = df.groupby('director')['revenue_adj'].sum()

# Sort the directors by revenue in descending order
top_directors_by_revenue = directors_revenue.sort_values(ascending=False)


pd.options.display.float_format = '{:,.2f}'.format

# Display the results
print("Top Directors by Number of Movies:")
print(top_directors_by_movies.head(10))

print("\nTop Directors by Revenue:")
print(top_directors_by_revenue.head(10))


print('-' * 40)

top_production_companies_by_movies = df['production_companies'].str.split('|', expand=True).stack().value_counts()
# Get the total revenue for each director
production_companies_revenue = df.groupby('production_companies')['revenue_adj'].sum()

# Sort the directors by revenue in descending order
top_production_companies_by_revenue = production_companies_revenue.sort_values(ascending=False)


pd.options.display.float_format = '{:,.2f}'.format

# Display the results
print("Top production_companies by Number of Movies:")
print(top_production_companies_by_movies.head(10))

print("\nTop  production_companies by Revenue:")
print(top_production_companies_by_revenue.head(10))




plt.figure(figsize=(10, 6))
plt.scatter(df['budget_adj'], df['runtime'], alpha=0.7, edgecolors='w')
plt.title('budget_adj vs. runtime', fontsize=16)
plt.xlabel('budget_adj', fontsize=12)
plt.ylabel('runtime', fontsize=12)
plt.legend(['Movies'])
plt.show()



plt.figure(figsize=(10, 6))
plt.scatter(df['popularity'], df['revenue_adj'], alpha=0.7, edgecolors='w')
plt.title('Popularity vs. Revenue of Movies', fontsize=16)
plt.xlabel('Popularity', fontsize=12)
plt.ylabel('Revenue', fontsize=12)
plt.legend(['Movies'])
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(df['budget_adj'], df['revenue_adj'], alpha=0.7, edgecolors='w')
plt.title('budget_adj vs. Revenue of Movies', fontsize=16)
plt.xlabel('budget_adj', fontsize=12)
plt.ylabel('Revenue', fontsize=12)
plt.legend(['Movies'])
plt.show()



# Assuming you have the 'genre_per_year' DataFrame with counts for each genre from 1960 to 2015
# If the column names are 'genre1', 'genre2', 'genre3', ... (replace with actual column names)

# Get the number of genres
num_genres = len(genre_per_year.columns)

# Set a custom color cycle using tab20 colormap
colors = plt.cm.tab20(np.linspace(0, 1, num_genres))

plt.figure(figsize=(12, 8))

# Plot each genre with a unique color from the custom cycle
for idx, genre in enumerate(genre_per_year.columns):
    plt.plot(genre_per_year.index, genre_per_year[genre], label=genre, color=colors[idx])

plt.title('Movie Releases by Genre (1960-2015)', fontsize=16)
plt.xlabel('Release Year', fontsize=12)
plt.ylabel('Number of Movies', fontsize=12)
plt.legend()
plt.grid(True)
plt.xticks(range(1960, 2016, 5))
plt.show()



columns_to_multiply = ['Crime', 'Drama', 'Western', 'Romance', 'History', 'Science Fiction', 'War', 'TV Movie', 'Foreign', 'Horror', 'Mystery', 'None', 'Animation', 'Adventure', 'Family', 'Comedy', 'Thriller', 'Music', 'Action', 'Fantasy', 'Documentary']
# Multiply the selected columns with the 'budget_adj' value
binary_df[columns_to_multiply] = binary_df[columns_to_multiply].multiply(binary_df['budget_adj'], axis=0)
genre_counts_by_year_budget = binary_df.groupby('release_year').sum()
genre_counts_by_year_budget=genre_counts_by_year_budget[['Crime', 'Drama', 'Western', 'Romance', 'History', 'Science Fiction', 'War', 'TV Movie', 'Foreign', 'Horror', 'Mystery', 'None', 'Animation', 'Adventure', 'Family', 'Comedy', 'Thriller', 'Music', 'Action', 'Fantasy', 'Documentary']]


num_genres = len(genre_counts_by_year_budget.columns)
# Set a custom color cycle using tab20 colormap
colors = plt.cm.tab20(np.linspace(0, 1, num_genres))
plt.figure(figsize=(12, 8))
# Plot each genre with a unique color from the custom cycle
for idx, genre in enumerate(genre_counts_by_year_budget.columns):
    plt.plot(genre_counts_by_year_budget.index, genre_counts_by_year_budget[genre], label=genre, color=colors[idx])

plt.title('Bugdet for Movie Releases by Genre (1960-2015)', fontsize=16)
plt.xlabel('Release Year', fontsize=12)
plt.ylabel('Budget ', fontsize=12)
plt.legend()
plt.grid(True)
plt.xticks(range(1960, 2016, 5))
plt.show()






columns_to_multiply = ['Crime', 'Drama', 'Western', 'Romance', 'History', 'Science Fiction', 'War', 'TV Movie', 'Foreign', 'Horror', 'Mystery', 'None', 'Animation', 'Adventure', 'Family', 'Comedy', 'Thriller', 'Music', 'Action', 'Fantasy', 'Documentary']
# Multiply the selected columns with the 'budget_adj' value
binary_df[columns_to_multiply] = binary_df[columns_to_multiply].multiply(binary_df['revenue_adj'], axis=0)
genre_counts_by_year_revenue = binary_df.groupby('release_year').sum()
genre_counts_by_year_revenue=genre_counts_by_year_revenue[['Crime', 'Drama', 'Western', 'Romance', 'History', 'Science Fiction', 'War', 'TV Movie', 'Foreign', 'Horror', 'Mystery', 'None', 'Animation', 'Adventure', 'Family', 'Comedy', 'Thriller', 'Music', 'Action', 'Fantasy', 'Documentary']]


num_genres = len(genre_counts_by_year_revenue.columns)
# Set a custom color cycle using tab20 colormap
colors = plt.cm.tab20(np.linspace(0, 1, num_genres))
plt.figure(figsize=(12, 8))
# Plot each genre with a unique color from the custom cycle
for idx, genre in enumerate(genre_counts_by_year_revenue.columns):
    plt.plot(genre_counts_by_year_revenue.index, genre_counts_by_year_revenue[genre], label=genre, color=colors[idx])

plt.title('Bugdet for Movie Releases by Genre (1960-2015)', fontsize=16)
plt.xlabel('Release Year', fontsize=12)
plt.ylabel('revenue ', fontsize=12)
plt.legend()
plt.grid(True)
plt.xticks(range(1960, 2016, 5))
plt.show()


