column_names_ratings = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings_df = pd.read_csv('/content/ml-1m/ml-1m/ratings.dat', sep='::', names=column_names_ratings, engine='python')

column_names_movies = ['movie_id', 'title', 'genres']
movies_df = pd.read_csv('/content/ml-1m/ml-1m/movies.dat', sep='::', names=column_names_movies, engine='python', encoding='latin-1')

merged_df = pd.merge(ratings_df, movies_df, on='movie_id')

pivot_table = merged_df.pivot_table(index='user_id', columns='title', values='rating')

while True:
    movie_title = input("Please enter a movie title: ")
    if movie_title in pivot_table.columns:
        break
    else:
        print(f"'{movie_title}' not found in the dataset. Please try again.")

movie_ratings = pivot_table[movie_title]
