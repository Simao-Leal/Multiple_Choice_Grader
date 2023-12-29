import tempfile
import os
from src.toolbox import get_student_list, get_reading_results
import string
from grading_function import grading_function

def evaluation_report_maker(exam_name, exam_date, name, number, ist_id, course, version,
                             answer_key, answers, correct, incorrect, unanswered, grade, path):
    colwidth = '11pt'
    def make_table(answer_key, answers, start):
        n = len(answer_key)
        res = '\n'
        res = r'\vspace*{0.5cm}'
        res += '\n\n'
        res += r'\begin{tabular}{|c|' + f'C{{{colwidth}}}|' * n + '}\n'
        res += r'\hline' + '\n'
        res += r'\textbf{Questão}' 
        for i in range(start, start + n):
            res += rf'&\textbf{{{i}}}'
        res += r'\\' + '\n'
        res += r'\hline' + '\n'
        res += r'\textbf{Chave}' 
        for key in answer_key:
            res += f'&{key}'
        res += r'\\' + '\n'
        res += r'\hline' + '\n'
        res += r'\textbf{Resposta}' 
        for answer, key in zip(answers, answer_key):
            res += '&' + ('\cellcolor{green!25}' if answer == key else '\cellcolor{red!25}') + f'{answer}'
        res += r'\\' + '\n'
        res += r'\hline' + '\n'
        res += r'\end{tabular}'
        return res

    tables = ""
    for i in range(0, len(answer_key), 20):
        tables += make_table(answer_key[i:i+20], answers[i:i+20], i + 1)

    with open("src/grader/evaluation_report_template.tex", 'r') as f:
        tex = f.read().format(exam_name=exam_name, exam_date=exam_date, name=name, number=number, course=course, version=version,
                             tables=tables, no_correct=correct, no_incorrect=incorrect, no_unanswered=unanswered, grade=grade, path=path)

    with tempfile.TemporaryDirectory() as directory:
        with open(f"{directory}/evaluation_report.tex", "w") as f:
            f.write(tex)
        
        os.system(f"pdflatex -output-directory={directory} --interaction=batchmode {directory}/evaluation_report.tex")
        os.system("mkdir -p output/evaluation_reports")
        os.system(f"cp {directory}/evaluation_report.pdf output/evaluation_reports/{ist_id}.pdf")
       
def grader(exam_name, exam_date, number_of_versions, number_of_questions, answer_keys):
    student_list = get_student_list()
    reading_results = get_reading_results(number_of_questions)

    #checking if all problems were fixed
    for number in reading_results:
        if number not in student_list:
            raise Exception(f"Number not found in student list: {number}. Correct reading_results.xls.")
        input_file, version, answers = reading_results[number]
        if version not in string.ascii_uppercase[:number_of_versions]:
            raise Exception(f"Wrong version for number {number}. Correct reading_results.xls.")

    #writing excel and evaluation reports
    for number in reading_results:
        ist_id, name, degree = student_list[number]
        input_file, version, answers = reading_results[number]

        #calculating grade 
        correct, incorrect, unanswered = 0, 0, 0
        for answer, key in zip(answers, answer_keys[version]):
            if answer == '':
                unanswered += 1
            else:
                if answer == key:
                    correct += 1
                else:
                    incorrect += 1
        
        grade = str(round(float(grading_function(correct, incorrect, unanswered)),1)).replace('.', ',')
        
        #write evaluation report
        evaluation_report_maker(exam_name, exam_date, name, number, ist_id, degree, version, answer_keys[version], answers, 
                                correct, incorrect, unanswered, grade, input_file)
        


if __name__ == '__main__':
    #evaluation_report_maker('Exame AMC Época Normal', '31/02/2024, 10:30', 'Simão', '92648', 'ist192648', 'LMAC', 'A', ['A', 'B', 'C', 'D', 'E'] + ['A'] * 39, ['A', 'D', 'E', '', 'A'] + ['A'] * 39, 2, 3, 0, '19,5', '/Users/simaoleal/Desktop/Multiple_Choice_Grader/input/Scanned from a Xerox Multifunction Printer001.jpg')
    grader('Exame AMC Época Normal', '31/02/2024, 10:30', 6, 10, {'A':['A']*10, 'B':['A']*10, 'C':['A']*10, 'D':['A']*10, 'E':['A']*10, 'F':['A']*10})