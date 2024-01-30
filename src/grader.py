import tempfile
import os
from src.toolbox import get_student_list, get_reading_results, header_style, text_style, red_center, green_center, integer_style, grade_style, center
import string
from config.grading_function import grading_function
import xlwt
import json
from tqdm import tqdm
import subprocess
import math

def round(x, n):
    #overloading python round function so that 0.5 always rounds up
    if x * 10 ** n - math.floor(x * 10 ** n) < 0.5:
        return math.floor(x * 10 ** n) / 10 ** n
    else:
        return math.ceil(x * 10 ** n) / 10 ** n

def evaluation_report_maker(file_name, exam_name, exam_date, name, number, course, version,
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
            res += '&' + ('\cellcolor{green!25}' if answer in key and answer != '' else '\cellcolor{red!25}') + f'{answer}'
        res += r'\\' + '\n'
        res += r'\hline' + '\n'
        res += r'\end{tabular}'
        return res

    tables = ""
    for i in range(0, len(answer_key), 20):
        tables += make_table(answer_key[i:i+20], answers[i:i+20], i + 1)

    with open("config/evaluation_report_template.tex", 'r') as f:
        tex = f.read().format(exam_name=exam_name, exam_date=exam_date, name=name, number=number, course=course, version=version,
                             tables=tables, no_correct=correct, no_incorrect=incorrect, no_unanswered=unanswered, grade=grade, path=path)

    with tempfile.TemporaryDirectory() as directory:
        with open(f"{directory}/evaluation_report.tex", "w") as f:
            f.write(tex)
        

        subprocess.run(["pdflatex", f"-output-directory={directory}", "-interaction=nonstopmode", f"{directory}/evaluation_report.tex"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        os.system("mkdir -p output/evaluation_reports")
        os.system(f"cp {directory}/evaluation_report.pdf output/evaluation_reports/{file_name}.pdf")
       
def grader(exam_name, exam_date, number_of_versions, number_of_questions, answer_keys):

    student_list = get_student_list()
    reading_results = get_reading_results(number_of_questions)
    grades = dict()
    email_adresses = dict()

    #checking if all problems were fixed
    for number in reading_results:
        if number not in student_list:
            raise Exception(f"Number not found in student list: {number}. Correct reading_results.xls.")
        input_file, version, answers = reading_results[number]
        if version not in string.ascii_uppercase[:number_of_versions]:
            raise Exception(f"Wrong version for number {number}. Correct reading_results.xls.")
        

    # initializing workbook    
    wb = xlwt.Workbook()
    detailed_sheet = wb.add_sheet('Pauta Detalhada')
    answer_keys_sheet = wb.add_sheet('Chaves de resposta')
    grades_sheet = wb.add_sheet('Pauta')

    #answer keys sheet
    header = ['Versão'] + [f'Q{i}' for i in range(1, number_of_questions + 1)]
    for i, t in enumerate(header):
        answer_keys_sheet.write(0, i, t, header_style)
    for row, version in enumerate(string.ascii_uppercase[:number_of_versions], start=1):
        answer_keys_sheet.write(row, 0, version, center)
        for col, answer in enumerate(answer_keys[version], start=1):
            answer_keys_sheet.write(row, col, answer, center)
    for column, width in enumerate([2000] + [1150] * number_of_questions):
        answer_keys_sheet.col(column).width = width


    #detailed sheet - contains only the students who did the exam
    header = ['Número', 'Nome', 'Curso', 'Versão'] + [f"Q{i}" for i in range(1, number_of_questions + 1)] + ['Corretas', 'Incorretas', 'NR/Inv.', 'Classificação']
    for i, t in enumerate(header):
        detailed_sheet.write(0, i, t, header_style)

    print('Writing excel and evaluation reports:')
    #writing excel and evaluation reports
    numbers = list(reading_results.keys())
    numbers.sort(key=lambda x: int(x))
    for row, number in enumerate(tqdm(numbers), start=1):
        email, name, degree = student_list[number]
        input_file, version, answers = reading_results[number]

        #calculating grade 
        correct, incorrect, unanswered = 0, 0, 0
        for answer, key in zip(answers, answer_keys[version]):
            if answer == '':
                unanswered += 1
            else:
                if answer in key:
                    correct += 1
                else:
                    incorrect += 1
        
        grade = round(float(grading_function(correct, incorrect, unanswered)),1)
        grades[number] = grade
        
        file_name = f"{exam_name.replace(' ', '_')}_{number}"
        #write evaluation report
        evaluation_report_maker(file_name, exam_name, exam_date, name, number, degree, version, answer_keys[version], answers, 
                                correct, incorrect, unanswered, str(grade).replace('.', ','), input_file)
        #save email adress
        email_adresses[file_name] = email
        
        #write to excel
        detailed_sheet.write(row, 0, number, text_style)
        detailed_sheet.write(row, 1, name)
        detailed_sheet.write(row, 2, degree)
        detailed_sheet.write(row, 3, version, center)
        for i, col in enumerate(range(4, 4 + number_of_questions)):
            if answers[i] in answer_keys[version][i] and answers[i] != '':
                detailed_sheet.write(row, col, answers[i], green_center)
            else:
                detailed_sheet.write(row, col, answers[i], red_center)
        col += 1
        detailed_sheet.write(row, col, correct, integer_style)
        col += 1
        detailed_sheet.write(row, col, incorrect, integer_style)
        col += 1
        detailed_sheet.write(row, col, unanswered, integer_style)
        col += 1
        detailed_sheet.write(row, col, grade, grade_style)

    for column, width in enumerate([2000,12000,2000,1800] + [1150] * number_of_questions + [2400] * 3 + [3010]):
        detailed_sheet.col(column).width = width


    #grades sheet - contains all the students, not just the ones who did the exam
    header = ['Número', 'Nome', exam_name] 
    for i, t in enumerate(header):
        grades_sheet.write(0, i, t, header_style)

    numbers = list(student_list)
    numbers.sort(key=lambda x: int(x))
    for row, number in enumerate(numbers, start=1):
        _, name, _ = student_list[number]
        grades_sheet.write(row, 0, number, text_style)
        grades_sheet.write(row, 1, name)
        if number in reading_results:
            grades_sheet.write(row, 2, grades[number], grade_style)

    for column, width in enumerate([2000,12000,3000]):
        grades_sheet.col(column).width = width

    #save excel
    wb.save('output/graded_results.xls')

    #save email adresses
    with open('output/evaluation_reports/email_adresses.json', 'w') as f:
        json.dump(email_adresses, f)

    print('Done!')

if __name__ == '__main__':
    evaluation_report_maker('urmom', 'Exame AMC Época Normal', '31/02/2024, 10:30', 'Simão', '92648', 'LMAC', 'A', ['A', 'ABCDE', 'C', 'D', 'E'] + ['A'] * 39, ['A', 'D', 'E', '', 'A'] + ['A'] * 39, 2, 3, 0, '19,5', '/Users/simaoleal/Desktop/AMC_Exame_1/input/teste001.jpg')
    #grader('Exame 1', '31/02/2024, 10:30', 6, 10, {'A':['A']*10, 'B':['A']*10, 'C':['A']*10, 'D':['A']*10, 'E':['A']*10, 'F':['A']*10})