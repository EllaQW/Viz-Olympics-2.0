#!/usr/bin/env python
# coding: utf-8

#Dataframe manipulation library
import pandas as pd


#Storing the movie information into a pandas dataframe
movies_df = pd.read_csv (r'C:\Users\eweng\Desktop\Viz Olympics 2.0\Netflix Data Tab.csv')
#Storing the user information into a pandas dataframe
ratings_df = pd.read_csv (r'C:\Users\eweng\Desktop\Viz Olympics 2.0\NetflixViewingHistory_data_revised.csv')


#Only take necessary columns from the Netflixx data
moviesCleansed_df= movies_df[['show_id', 'title', 'listed_in']]
moviesCleansed_df.head()
moviesCleansed_df['listed_in'].dtypes()

#Every genre is separated by a comma so we simply have to call the split function on ', '
moviesCleansed_df.loc['listed_in'] = moviesCleansed_df.listed_in.str.split(', ')
moviesCleansed_df.head()
print(moviesCleansed_df)

#Copying the movie dataframe into a new one since we won't need to use the genre information in our first case.
moviesWithGenres_df = moviesCleansed_df.copy()

#For every row in the dataframe, iterate through the list of genres and place a 1 into the corresponding column
for index, row in moviesCleansed_df.iterrows():
    for genre in row['listed_in']:
        moviesWithGenres_df.at[index, genre] = 1
#Filling in the NaN values with 0 to show that a movie doesn't have that column's genre
moviesWithGenres_df = moviesWithGenres_df.fillna(0)
moviesWithGenres_df.head()



#rename columns for joining the two tables together
ratings_df = ratings_df.rename(columns={'Title': 'title'})
ratings_df.head()



#Filtering out the movies by title
inputId = movies_df[movies_df['title'].isin(ratings_df['title'].tolist())]
#Then merging it so we can get the show_id. It's implicitly merging it by title.
inputMovies = pd.merge(inputId, ratings_df)
inputMovies = inputMovies[['show_id', 'title', 'Rating']]
inputMovies.head()


#Filtering out the movies from the input
userMovies = moviesWithGenres_df[moviesWithGenres_df['show_id'].isin(inputMovies['show_id'].tolist())]
userMovies.head()


#Resetting the index to avoid future issues
userMovies = userMovies.reset_index(drop=True)
#Dropping unnecessary issues due to save memory and to avoid issues
userGenreTable = userMovies.drop('show_id', 1).drop('title', 1).drop('listed_in', 1)
userGenreTable.head()


#Start learning the user preference
#Dot produt to get weights
userProfile = userGenreTable.transpose().dot(inputMovies['Rating'])
#The user profile
userProfile


#Now let's get the genres of every movie in our original dataframe
genreTable = moviesWithGenres_df.set_index(moviesWithGenres_df['show_id'])
#And drop the unnecessary information
genreTable = genreTable.drop('show_id', 1).drop('title', 1).drop('listed_in', 1)
genreTable.head()


#Multiply the genres by the weights and then take the weighted average
recommendationTable_df = ((genreTable*userProfile).sum(axis=1))/(userProfile.sum())
recommendationTable_df.head()


#Sort our recommendations in descending order
recommendationTable_df = recommendationTable_df.sort_values(ascending=False)
#Just a peek at the values
recommendationTable_df.head()


#The final recommendation table
movies_df.loc[movies_df['show_id'].isin(recommendationTable_df.head(20).keys())]

