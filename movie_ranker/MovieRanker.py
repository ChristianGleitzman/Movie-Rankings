import math
from PyQt5 import QtWidgets, uic
import sys
import requests
from bs4 import BeautifulSoup
import re
from sqlite3 import *

#Webscrapes movie data from the top 250 movies on the imdb website
#Returns the movie data in a 2D list with an initial elo of 1500
def get_movie_data():
    # Downloading imdb top 250 movie's data
    url = 'http://www.imdb.com/chart/top'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    movies = soup.select('td.titleColumn')
    crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]

    # create a empty movies_list for storing movie information
    movies_list = []
    
    # Iterating over movies to extract
    # each movie's details
    for index in range(0, len(movies)):
        movie_string = movies[index].get_text()
        movie = (' '.join(movie_string.split()).replace('.', ''))
        movie_title = movie[len(str(index))+1:-7]
        if len(movie_title) > 20:
            temp = movie_title.split(" ")
            movie_title = ""
            for i in range(len(temp)-1):
                movie_title += temp[i] + " "
                if i == len(temp) // 2:
                    movie_title += "\n"
            movie_title += temp[-1]
        year = int(re.search('\((.*?)\)', movie_string).group(1))
        if year >= 1970:
            data = [movie_title,
                    year,
                    crew[index],
                    1500
            ]
            movies_list.append(data)
    return movies_list
    
K = 32

class Database:
    def __init__(self):
        #Database name set to database file name
        self.__dbname = 'movies.db'
    def connection(self):
        #Creates connection to database file
        con = connect(self.__dbname)
        cur = con.cursor()
        return con,cur
    def executeStatement(self, query, args=None):
        con,cur = self.connection()
        #Executes a given query on the database
        if not args:
            cur.execute(query)
        else:
            cur.execute(query, args)
        #Any data fetched from the database is assigned to 'selectedData'
        selectedData = cur.fetchall()
        #Any changes to the contents of the database are committed
        con.commit()
        #Connection to the database is closed
        con.close()
        #Any selected data is returned
        return selectedData
    def select(self, fields, table, selectBy=None, args=None):
        #Constructs a select statement based on arguments entered
        if not selectBy:
            query = f'SELECT {fields} FROM {table}'
        else:
            query = f'''SELECT {fields} FROM {table}
            WHERE {selectBy} = ?'''
        #returns the results of the execution of the query
        return self.executeStatement(query, args)
    #Calls the function to webscrape movie data and inserts this data into the movie database
    def save_movie_data(self):
        movies_list = get_movie_data()
        query = '''INSERT INTO tblMovies(title, year, cast, elo)
            VALUES (?,?,?,?)'''
        for movie in movies_list:
            self.executeStatement(query, movie)     

class Ranker(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ranker, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('MovieRanker.ui',self) #Load the ui file
        
        #Handles the events of buttons being clicked
        self.movieOneButton.clicked.connect(lambda: self.movie_selected(1))
        self.movieTwoButton.clicked.connect(lambda: self.movie_selected(2))

        #Handles the event of a tab being changed
        self.tabWidget.currentChanged.connect(self.onChange)

        #Initialises the database with movie data and sets up menu tabs
        self.initialise_database()
        self.setup_comparison()
        self.show()
    #Creates an instance of the database class and calls the method to fetch movie data if it hasn't been done before
    def initialise_database(self):
        self.db = Database()
        current_movies = self.db.select("movieID", "tblMovies")
        if len(current_movies) == 0:
            self.db.save_movie_data()
    #Sets up a movie comparison/matchup by selecting two random movies from the database and adding them to the window
    def setup_comparison(self):
        random_movies = self.db.executeStatement("SELECT * FROM tblMovies ORDER BY RANDOM() LIMIT 2;")
        self.movie1 = random_movies[0]
        self.movie2 = random_movies[1]
        self.cast1 = self.movie1[3].split(", ")
        self.cast2 = self.movie2[3].split(", ")
        self.movieOneButton.setText(self.movie1[1] + "\n(" + str(self.movie1[2]) + ")\n\nCast:\n" + self.cast1[0] +"\n"+ self.cast1[1] +"\n"+ self.cast1[2])
        self.movieTwoButton.setText(self.movie2[1] + "\n(" + str(self.movie2[2]) + ")\n\nCast:\n" + self.cast2[0] +"\n"+ self.cast2[1] +"\n"+ self.cast2[2])
    #Decides the winner of the matchup based on the button selected by the user
    def movie_selected(self, winner):
        if winner == 1:
            self.update_movies(list(self.movie1), list(self.movie2))
            self.lblOutcome.setText(f"{self.movie1[1]} won that matchup!")
        else:
            self.update_movies(list(self.movie2), list(self.movie1))
            self.lblOutcome.setText(f"{self.movie2[1]} won that matchup!")
        self.setup_comparison() 
    #Updates the elo of the winner and loser and saves these new elos to the database
    def update_movies(self, winner, loser):
        expected_score_winner = 1 / (1 + math.pow(10, (loser[4] - winner[4]) / 400))
        expected_score_loser = 1 / (1 + math.pow(10, (winner[4] - loser[4]) / 400))
        winner[4] += K * (1 - expected_score_winner)
        loser[4] += K * (0 - expected_score_loser)
        self.db.executeStatement('''UPDATE tblMovies
            SET elo = ?
            WHERE movieID = ?''', (winner[4], winner[0]))
        self.db.executeStatement('''UPDATE tblMovies
            SET elo = ?
            WHERE movieID = ?''', (loser[4], loser[0]))
    #@pyqtSlot()  
    def onChange(self, index):
        #Calls a method based on what the current tab has been changed to
        self.lblOutcome.setText("")
        if index == 1:
            self.listFavourite()
        elif index == 2:
            self.listWorst()
    #Displays a user's favourite movies
    def listFavourite(self):
        text = self.createList("DESC")
        self.lblFavouriteMovies.setText(text)
    #Displays a user's least favourite movies
    def listWorst(self):
        text = self.createList("ASC")
        self.lblWorstMovies.setText(text)
    #Creates a least or most favourite movie list to display
    def createList(self, order):
        movies = self.db.executeStatement(f"SELECT title, year FROM tblMovies ORDER BY elo {order} LIMIT 10;")
        text = ""
        for i in range(len(movies)):
            curr_string = "{}) {} ({})\n".format(i+1, movies[i][0], movies[i][1])
            text += curr_string
        return text

def main():
    #Initialises and displays window
    app = QtWidgets.QApplication(sys.argv)
    window = Ranker()
    app.exec_()
    

main()