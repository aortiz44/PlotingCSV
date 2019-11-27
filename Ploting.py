import plotly.graph_objects as go
import csv
import os

CORRECT_COLOR = 'rgb(0,191,255)'
INCORRECT_COLOR = 'rgb(232,54,54)'
SKIPPED_COLOR = 'rgb(105,105,105)'


class ResultPlotter:

    def __init__(self):
        pass

    def new_plot_stacked(self, latest_set_results, project_num=0):
        graph_title = "Project " + str(project_num)
        xvals = []
        result_answer_list = []
        correct = []
        incorrect = []
        skipped = []
        with open(latest_set_results) as file:
            filereader = csv.reader(file, delimiter='\n')
            count = 0
            for row in filereader:
                if "Set" in row[0] or count >= 1:
                    count += 1
                    str_line = row[0]
                    if len(str_line) > 20:
                        str_line = str_line.replace('"', '')
                    if "Problems" in str_line:
                        if "Set" not in str_line:
                            str_line = str_line.replace(':', '')
                            str_line = str_line.replace('{', '')
                            result_answer_list.append(AnswerResult(str_line))
                    self.helperMethod(str_line, result_answer_list)

        result_answer_list.sort(key=lambda x: (x.problem_set, x.problem_name))
        fig = []
        for element in result_answer_list:
            print element.name, "<--", element.incorrect, element.correct, element.skipped
            print element.problem_name
            incorrect.append(element.incorrect)
            correct.append(element.correct)
            skipped.append(element.skipped)
            xvals.append(element.name)
        dataArr = [go.Bar(name="correct", x=xvals, y=correct, marker_color=CORRECT_COLOR),
                   go.Bar(name="incorrect", x=xvals, y=incorrect, marker_color=INCORRECT_COLOR),
                   go.Bar(name="skipped", x=xvals, y=skipped, marker_color=SKIPPED_COLOR)]
        figure = go.Figure(data=dataArr)
        figure.update_layout(barmode='stack')
        figure.update_layout(
            title=go.layout.Title(
                text=graph_title,
                xref="paper",
                x=0))
        figure.show()

    def helperMethod(self, str_line, result_answer_list):
        flag = 0
        if "Correct" in str_line:
            str_line = str_line.replace('Correct: ', '')
            flag = 1
        if "Skipped" in str_line:
            str_line = str_line.replace('Skipped: ', '')
            flag = 2
        if "Incorrect" in str_line:
            str_line = str_line.replace('Incorrect: ', '')
            flag = 3
        if flag > 0:
            str_line = str_line.replace(',', '')
            value = int(str_line)
            element = result_answer_list[-1]
            if flag == 1:
                element.SetCorrect(value)
            if flag == 2:
                element.SetSkipped(value)
            if flag == 3:
                element.SetIncorrect(value)

    def plotAll(self):
        self.new_plot_stacked('ResultsProject3_Attempt1_Full.csv', 3)
        self.new_plot_stacked('ResultsProject3_Attempt2_Full.csv', 3)
        self.new_plot_stacked('ResultsProject3_Attempt3_Full.csv', 3)
        self.new_plot_stacked('ResultsProject3_Attempt4_Full.csv', 3)
        self.new_plot_stacked('ResultsProject3_Attempt5_Full.csv', 3)

        # self.new_plot_stacked('ResultsProject2_Attempt3_Full.csv')
        # self.new_plot_stacked('ResultsProject2_Attempt4_Full.csv')
        # self.new_plot_stacked('ResultsProject2_Attempt5_Full.csv')
        # self.new_plot_stacked('ResultsProject2_Attempt6_Full.csv')


class AnswerResult:
    def __init__(self, name):
        name = str(name)
        name = name.strip()
        self.name = name
        name = name.split(' ')
        self.problem_set = name[2]
        self.problem_name = name[0]
        self.incorrect = 0
        self.skipped = 0
        self.correct = 0
        pass

    def SetIncorrect(self, value):
        self.incorrect = value

    def SetCorrect(self, value):
        self.correct = value

    def SetSkipped(self, value):
        self.skipped = value


if __name__ == "__main__":
    plotter = ResultPlotter()
    plotter.plotAll()
