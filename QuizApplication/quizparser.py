import xml.sax
from quiz import *
from enum import Enum, unique

@unique
class QuizParserState(Enum):
    """
    This class represents an enumeration of the state of the quiz parser. Unique numerical values
    are assigned to each corresponding parsing state.
    """

    IDLE = 0
    PARSE_QUIZ = 1
    PARSE_DESCRIPTION = 2
    PARSE_QUESTION = 3
    PARSE_QUEST_TEXT = 4
    PARSE_ANSWER = 5

class QuizParser(xml.sax.ContentHandler):
    """
    This class holds the functionality of parsing a folder with multiple .xml files into a list of multiple
    corresponding quiz objects.

    ...

    Attributes:
        new_quiz (Quiz) : a new quiz object placeholder
        _parse_state (QuizParserState) : the current parse state
        _current_question (Question) : the current question
        _current_answer (Answer) : the current answer
    """

    def __init__(self):
        """
        Initializes attributes
        """

        self.new_quiz = Quiz()

        self._parse_state = QuizParserState.IDLE
        self._current_question = None
        self._current_answer = None

    def parse_quiz(self, quizpath):
        """
        Opens the quiz using ther quizpath and gets all the text form the file

        Parameters:
            quizpath (str) : the path where the quiz is located
        """

        quiztext = ""
        with open (quizpath, "r") as quizfile:
            if quizfile.mode == "r":
                quiztext = quizfile.read()
    
        xml.sax.parseString(quiztext, self)

        return self.new_quiz
    
    def startElement(self, tagname, attrs):
        """
        Performs the proper encoding of the quiz based on the starting element in the given text

        Parameters:
            tagname (str) : the name of the tag that the text begins with
            attrs (list) : a list of the attributes under the tag
        """

        if tagname == "QuizML":
            self._parse_state = QuizParserState.PARSE_QUIZ
            self.new_quiz.name = attrs["name"]
        elif tagname == "Description":
            self._parse_state = QuizParserState.PARSE_DESCRIPTION
        elif tagname == "Question":
            self._parse_state = QuizParserState.PARSE_QUESTION
            if attrs["type"] == "multichoice":
                self._current_question = QuestionMC()
            elif attrs["type"] == "tf":
                self._current_question = QuestionTF()
            self._current_question.points = int(attrs["points"])
            self.new_quiz.total_points += self._current_question.points
        elif tagname == "QuestionText":
            self._parse_state = QuizParserState.PARSE_QUEST_TEXT
            self._current_question.correct_answer = attrs["answer"]
        elif tagname == "Answer":
            self._current_answer = Answer()
            self._current_answer.name = attrs["name"]
            self._parse_state = QuizParserState.PARSE_ANSWER

    
    def endElement(self, tagname):
        """
        Performs the proper encoding of the quiz based on the ending element in the given text

        Parameters:
            tagname (str) : the name of the tag that the text ends with
        """
        if tagname == "QuizML":
            self._parse_state = QuizParserState.IDLE
        elif tagname == "Description":
            self._parse_state = QuizParserState.PARSE_QUIZ
        elif tagname == "Question":
            self.new_quiz.questions.append(self._current_question)
            self._parse_state = QuizParserState.PARSE_QUIZ
        elif tagname == "QuestionText":
            self._parse_state = QuizParserState.PARSE_QUESTION
        elif tagname == "Answer":
            self._current_question.answers.append(self._current_answer)
            self._parse_state = QuizParserState.PARSE_QUESTION

    
    def characters (self, chars):
        """
        Processes the given characters based on the parsing state and performs the corresponding
        actions
        """

        if self._parse_state == QuizParserState.PARSE_DESCRIPTION:
            self.new_quiz.description += chars
        if self._parse_state == QuizParserState.PARSE_QUEST_TEXT:
            self._current_question.text += chars
        if self._parse_state == QuizParserState.PARSE_ANSWER:
            self._current_answer.text += chars
