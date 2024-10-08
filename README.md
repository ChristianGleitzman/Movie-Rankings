# Movie-Rankings

This program is a movie ranking system that uses the Elo rating system to rank movies based on user opinions during match-ups.

## What the program does

- The program starts with a list of movies and their attributes (e.g. title, year, director, etc.) which have been scraped from a movie database website. 
Each movie is saved to a database and initializes the Elo rating for each movie to 1500.

- The program will then prompt the user to compare two movies and input their opinion on which movie is better using a user interface created using PyQt5.

- Based on the user's input, the program updates the Elo ratings of the two movies using the Elo rating system formula and saves these changes to the database.

- The user can continue to complete movie matchups or view their least or most favourite movies.

## Screenshots

![Matchup](https://github.com/ChristianGleitzman/Movie-Rankings/blob/main/movie_ranker/matchup.PNG)
![Favourite Movies](https://github.com/ChristianGleitzman/Movie-Rankings/blob/main/movie_ranker/favourite_movies.PNG)

## Improvements

It is important to note that the ranking is based on user opinions, so the ranking may be biased towards certain movies or genres. This can be improved by gathering more user opinions or by taking into account additional attributes for each movie. The more matchups that are completed by a specific user for an instance of the database, the more biased the ratings will be towards a specific user. A way to combat this would be to have a login system with different elo rankings for different users to have more personalised movie rankings. Additional improvements could be integrating a system where a user could share their movie rankings via email or social media. A final improvement that could be made would be to have a manual movie entry form that takes a movie title from the user that they have definitely seen before (a user may not have seen a movie that has been webscraped) and then a website can be webscraped to attain additional movie information such as year/cast. This would help in making their movie rankings more personalised.
