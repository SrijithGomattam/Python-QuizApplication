from quizmanager import QuizManager


class QuizApp:
    """
    This class represents the main quiz application and proivdes methods to display information to the user
    and perform a corresponding task based on the user selection.

    ...

    Attributes:
        username (str) : the username of the quiz taker
        qm (QuizManager) : a Quiz Manager object that performs the delegated tasks
    """

    QUIZ_FOLDER = "Quizzes"

    def __init__(self):
        """
        Initializes attributes
        """

        self.username = ""
        self.qm = QuizManager(QuizApp.QUIZ_FOLDER)

    def startup(self):
        """
        Asks for and prints the user's name
        """
        self.greeting()

        self.username = input("What is your name? ")
        print(f"Welcome, {self.username}!")

    def greeting(self):
        """
        Prints out the greeting message
        """

        print("---------------------------------------------")
        print("--------Welcome to the Quiz Application------")
        print("---------------------------------------------")
        print()

    def menu_header(self):
        """
        Prints the menu header
        """

        print("---------------------------------------------")
        print("Please make a selection")
        print("(M): Repeat this menu")
        print("(L): List all possible quizzes")
        print("(T): Take a quiz")
        print("(E): Exit the program")
        print("---------------------------------------------")


    def menu_error_message(self):
        """
        Prints and error message that corresponds to when an invalid selection is typed
        """

        print("That is not a valid seleciton. Please try again")
    
    def goodbye(self):
        """
        Prints the goodbye message
        """
        print("---------------------------------------------")
        print("    Thanks for using the Quiz Application!")
        print("---------------------------------------------")

    def menu(self):
        """
        Controls the application. Presents the choices for the user and calls the corresponding
        functions based on the user selection.
        """

        self.menu_header()

        selection = ""
        while(True):
            selection = input("Selection: ")
            
            if len(selection) == 0:
                self.menu_error_message()
                continue

            selection = selection.capitalize()

            if selection[0] == 'E':
                self.goodbye()
                break
            elif selection[0] == 'M':
                self.menu_header()
                continue
            elif selection[0] =='L':
                print("\nAvaliable Quizzes Are: ")
                self.qm.list_quizes()                
                print("---------------------------------------------")
            elif selection[0] == 'T':
                try:
                    quiznum = int(input("Quiz Number: "))
                    print(f"You have selected quiz {quiznum}")

                    self.qm.take_quiz(quiznum, self.username)
                    self.qm.print_results()

                    dosave = input("Save the results? (y/n): ")
                    dosave = dosave.capitalize()
                    if (len(dosave) > 0 and dosave[0] == 'Y'):
                        self.qm.save_results()

                except:
                    self.menu_error_message()
            else:
                self.menu_error_message()

    def run(self):
        self.startup()
        self.menu()

# Start the app
if __name__ == "__main__":
        app = QuizApp()
        app.run()

