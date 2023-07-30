import os.path
import os
import quizparser
import datetime

class QuizManager:
    """
    This class represents a manaager for the quiz and performs all the funcitonalities the user could possibly
    request whern using the program.

    ...

    Attributes:
        quizfolder (str) : the path of the folder containig the quizzes
        the_quiz (Quiz) : the quiz that is being taken
        quizzes (dict) : a dictionary containing all of the quizzes
        results (tuple) : a tuple containing all the final resutls of the quiz
        quiztaker (str) : the name of the user taking the quiz
    """

    def __init__(self, quizfolder):
        """
        Initializes attributes and checks if the given folder exists

        Parameters:
            quizfolder (str) : the path of the folder containig the quizzes

        Raises:
            FileNotFoundError if the folder does not exist
        """
        self.quizfolder = quizfolder
        self.the_quiz = None
        self.quizzes = dict()
        self.results = None
        self.quiztaker = ""

        if (os.path.exists(quizfolder) == False):
            raise FileNotFoundError("The quiz folder does not exist")
        
        self._build_quiz_list()

    def _build_quiz_list(self):
        """
        Parses through the given folder and uses a quizparser to make a quiz out of each file. Then
        assigns an index to each of these quizzes
        """

        dircontents = os.scandir(self.quizfolder)

        for i, f in enumerate(dircontents):
            if f.is_file():
                parser = quizparser.QuizParser()
                self.quizzes[i+1] = parser.parse_quiz(f)

    def list_quizes(self):
        """
        Lists the quizzes found in the given folder
        """

        for k, v in self.quizzes.items():
            print(f"({k}): {v.name}")

    def take_quiz(self, quizid, username):
        """
        Calls the take_ quiz method from the quiz class onto the quiz object created within this class

        Parameters:
            quizid (int) : the id number of the quiz
            username (str) : the username
        """

        self.quiztaker = username
        self.the_quiz = self.quizzes[quizid]
        self.results = self.the_quiz.take_quiz()
        return(self.results)

    def print_results(self):
        """
        Prints the results of the current quiz
        """

        self.the_quiz.print_results(self.quiztaker)

    def save_results(self):
        """
        Writes and saves the results to a file with a unique name based on the time saved
        """
        today = datetime.datetime.now()
        filename = f"Results/QuizResults_{today.year}_{today.month}_{today.day}.txt"

        n = 1
        while(os.path.exists(filename)):
            filename = f"QuizResults_{today.year}_{today.month}_{today.day}_{n}.txt"
            n = n + 1

        with open(filename, "w") as f:
            self.the_quiz.print_results(self.quiztaker, f)
