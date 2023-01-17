# Movie-Rankings

This program is a movie ranking system that uses the Elo rating system to rank movies based on user opinions during match-ups.

## What the program does

- The program starts with a list of movies and their attributes (e.g. title, year, director, genre, etc.) which have been scraped from a movie database website. 
Each movie is saved to a database and initializes the Elo rating for each movie to 1500.

- The program then prompts the user to compare two movies and input their opinion on which movie is better using a user interface created using PyQt5.

- Based on the user's input, the program updates the Elo ratings of the two movies using the Elo rating system formula and saves these changes to the database.

- The user can continue to complete movie matchups or view their least or most favourite movies.

## Screenshots

## Improvements

It is important to note that the ranking is based on user opinions, so the ranking may be biased towards certain movies or genres. This can be improved by gathering more user opinions or by taking into account additional attributes for each movie. The more matchups that are completed by a specific user for an instance of the database, the more biased the ratings will be towards a specific user. A way to combat this would be to have a login system with different elo rankings for different users to have more personalised movie rankings. Additional improvements could be integrating a system where a user could share their movie rankings via email or social media.
