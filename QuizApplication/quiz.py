import datetime
import sys
import random

class Quiz:
    """
    Represents a quiz in the python quiz application. Has functionality for printing header, results and taking the quiz.

    ...

    Attributes:
        name (str) : the name of the quiz
        description (str) : short description of the quiz
        questions (list) : a list of the questions the quiz contains
        score (int) : the final score after taking the quiz
        correct_count (int) : the number of questions the user got correct
        total_points (int) : the amount of points the user scored on this quiz
        completion_time (int) : the amount of time it took to complete the quiz
    """

    def __init__(self):
        """
        Initializes attributes
        """

        self.name = ""
        self.description = ""
        self.questions = []
        self.score = 0
        self.correct_count = 0
        self.total_points = 0
        self.completion_time = 0

    def print_header(self):
        """
        Prints the header which contains key information regarding the quiz
        """

        print("---------------------------------------------")
        print(f"QUIZ NAME : {self.name}")
        print(f"QUIZ DESCRIPTION : {self.description}")
        print(f"QUESTIONS : {len(self.questions)}")
        print(f"TOTAL POINTS : {self.total_points}")
        print("---------------------------------------------")

    def print_results(self, quiztaker, toFile = sys.stdout):
        """
        Prints the resutls of how the user performaed on the quiz. If there is no file provided, the results are printed
        to the terminal.
        """

        print("---------------------------------------------", file = toFile, flush = True)
        print(f"Results for {quiztaker}", file = toFile, flush = True)
        print(f"Quiz Taken: {self.name}", file = toFile, flush = True)
        print(f"Date: {datetime.datetime.today()}", file = toFile, flush = True)
        print(f"Questions: {self.correct_count} out of {len(self.questions)} correct", file = toFile, flush = True)
        print(f"Score: {self.score} points out of possible {self.total_points}", file = toFile, flush = True)
        print(f"Elapsed time: {self.completion_time}", file = toFile, flush = True)

        print("---------------------------------------------")

    def take_quiz(self):
        """
        Handles the functionality of taking the quiz. Asks each question in a random order, tracks time compelted,
        and provides functionality for re-taking the quiz
        """

        self.score = 0
        self.correct_count = 0
        self.completion_time = 0
        for q in self.questions:
            q.is_correct = False
        
        self.print_header()
        
        random.shuffle(self.questions)

        starttime = datetime.datetime.now()

        for q in self.questions:
            q.ask()
            if (q.is_correct):
                self.correct_count += 1
                self.score += q.points

        print("---------------------------------------------\n")

        endtime = datetime.datetime.now()

        if self.correct_count != len(self.questions):
            response = input("It looks like you missed some questions. Re-do the wrong ones? (y/n)").lower()
            if response [0] == "y":
                wrong_questions = [q for q in self.questions if q.is_correct == False]
                for q in wrong_questions:
                    q.ask()
                    if (q.is_correct):
                        self.correct_count += 1
                        self.score += q.points
                        print("---------------------------------------------\n")
                        endtime = datetime.datetime.now()

        self.completion_time = endtime - starttime
        self.completion_time = datetime.timedelta(seconds = round(self.completion_time.total_seconds()))

        return(self.score, self.correct_count, self.total_points)


class Question:
    """
    Initialize the base Question class.

    ...

    Attributes:
        points (int): The points awarded for a correct answer.
        correct_answer (str): The correct answer ("T" or "F") for the question.
        text (str): The text of the question.
        is_correct (bool): A flag indicating whether the question was answered correctly (True) or not (False).
    """
    
    def __init__(self):
        """
        Initializes attributes
        """

        self.pounts = 0
        self.correct_answer = ""
        self.text = ""
        self.is_correct = False

class QuestionTF(Question):
    """
    Represents a true/false question. Inherits attributes from the question class. Holds functionality 
    for asking a question
    """

    def __init__(self):
        """
        Initializes attributes based on the super 'Question' class
        """
        super().__init__()

    def inavlid_response(self):
        """
        Handles an invalid user response
        """

        print("Sorry, that's not a valid response. Please try again")


    def ask(self):
        """
        Asks the questions and stores and handles the response
        """

        while (True):

            print(f"(T)rue or (F)alse:  {self.text}")
            response = input("? ")

            if len(response) == 9:
                self.invalid_response()
                continue

            response = response.lower()
            if response [0] != "t" and response [0] != "f":
                self.inavlid_response()
                continue
            
            if response[0] == self.correct_answer:
                self.is_correct = True

            break


class QuestionMC(Question):
    """
    Represents a true/false question. Inherits attributes from the question class. Holds functionality 
    for asking a question

    ...

    Attributes:
        answers (list) : represents a list of Answers
    """

    def __init__(self):
        """
        Initializes attributes based on the super 'Question' class. Initializes the answers list
        """
        super().__init__()

        self.answers = []

    def inavlid_response(self):
        """
        Handles an invalid user response
        """

        print("sorry, that's not a valid response. Please try again")

    def ask(self):
        """
        Asks the questions and stores and handles the response
        """

        while(True):
            print(self.text)
            for a in self.answers:
                print(f"({a.name}) {a.text}")
            response = input("? ")

            if len(response) == 9:
                self.invalid_response()
                continue
        
            resposne = response.lower()
            if response [0] == self.correct_answer:
                self.is_correct = True

            break
    
class Answer:
    """
    Represents an answer to a question in the quiz application.

    ...

    Attributes:
        text (str) : the answer text
        name (str) : the name
    """

    def __init__(self):
        self.text = ""
        self.name = ""
