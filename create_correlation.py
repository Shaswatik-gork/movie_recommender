import os
import pandas as pd
import numpy as np 
ratings_file_path_option1 = '/content/ml-1m/ml-1m/ratings.dat'
ratings_file_path_option2 = './ml-1m/ratings.dat'

found_ratings_file = None
if os.path.exists(ratings_file_path_option1):
    found_ratings_file = ratings_file_path_option1
elif os.path.exists(ratings_file_path_option2):
    found_ratings_file = ratings_file_path_option2


if found_ratings_file:
    movies_file_path = os.path.join(os.path.dirname(found_ratings_file), 'movies.dat')

    if not os.path.exists(movies_file_path):
         print(f"Error: The file {movies_file_path} was not found.")
    else:
        column_names_ratings = ['user_id', 'movie_id', 'rating', 'timestamp']
        ratings_df = pd.read_csv(found_ratings_file, sep='::', names=column_names_ratings, engine='python')

        column_names_movies = ['movie_id', 'title', 'genres']
        movies_df = pd.read_csv(movies_file_path, sep='::', names=column_names_movies, engine='python', encoding='latin-1')

        # Ensure 'movie_id' columns have the same data type before merging
        ratings_df['movie_id'] = ratings_df['movie_id'].astype(str)
        movies_df['movie_id'] = movies_df['movie_id'].astype(str)


        merged_df = pd.merge(ratings_df, movies_df, on='movie_id')

        pivot_table = merged_df.pivot_table(index='user_id', columns='title', values='rating')


        while True:
            movie_title = input("Please enter a movie title: ")
            if movie_title in pivot_table.columns:
                break
            else:
                print(f"'{movie_title}' not found in the dataset. Please try again.")


        movie_ratings = pivot_table[movie_title]

        # Calculate correlation. RuntimeWarnings related to division by zero or invalid values
        # can occur when there is insufficient data for correlation (e.g., very few common raters).
        # These warnings are often harmless as the resulting NaN values are dropped afterwards.
        similar_movies = pivot_table.corrwith(movie_ratings)


        corr_df = pd.DataFrame(similar_movies, columns=['Correlation'])
        corr_df.dropna(inplace=True)

        # Calculate the number of ratings for each movie
        movie_ratings_count = merged_df.groupby('title')['rating'].count().rename('num of ratings')

        # Merge the correlation results with the number of ratings
        corr_with_counts = corr_df.join(movie_ratings_count)

        # Filter for movies with a sufficient number of ratings
        # Using a threshold of 100, but this can be adjusted
        rating_threshold = 100
        filtered_corr = corr_with_counts[corr_with_counts['num of ratings'] > rating_threshold]

        # Sort the filtered DataFrame by 'Correlation'
        sorted_corr = filtered_corr.sort_values('Correlation', ascending=False)

        # Display the top N movies (e.g., top 10)
        top_n = 10
        print(f"\nTop {top_n} movies correlated with '{movie_title}':")
        display(sorted_corr.head(top_n))

else:
    print("Error: Neither ./ml-1m/ratings.dat nor ./ratings.dat were found.")
