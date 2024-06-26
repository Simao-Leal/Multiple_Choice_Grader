import glob
import os
import csv
import xlwt
import xlrd
import string
import subprocess
from src.toolbox import remove_left_zeros, get_student_list, red, yellow, header_style, right_aligned, text_style


def reader(number_of_questions, number_of_answers, number_of_versions):
    print('Reading...')
    student_list = get_student_list()

    #OMR analysis 
    os.system("rm -f -r aux/OMR_output")
    subprocess.run(["python", "src/OMRChecker-master/main.py", "--inputDir", "aux/OMR_input", "--outputDir", "aux"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    os.system("mv aux/input aux/OMR_output")

    #writing results to excel
    file = glob.glob('aux/OMR_output/Results/Results*.csv')[0]
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Results')
    header = ["Input File", "Number", "Name", "Degree", "Version"] + [f"Q{i}" for i in range(1, number_of_questions + 1)]
    for i, t in enumerate(header):
        ws.write(0, i, t, header_style)

    with open(file, mode='r') as csvfile:
        results = csv.reader(csvfile)
        already_read = []

        next(results)

        error_counter = 0
        warning_counter = 0

        for i, line in enumerate(results, start=1):
            _, input_file, _, _, version, number, *answers = line

            ws.write(i, 0, input_file, right_aligned)

            number = remove_left_zeros(number)

            if number in student_list:
                if number not in already_read:
                    _, name, degree = student_list[number]
                    ws.write(i, 1, number, text_style)
                    already_read.append(number)
                else:
                    error_counter += 1
                    _, name, degree = "DUPLICATE", "THIS STUDENT NUMBER WAS SEEN TWICE", "DUPLICATE"
                    ws.write(i, 1, number, red)
            else:
                error_counter += 1
                name, degree = "STUDENT NUMBER NOT FOUND IN STUDENT LIST", "NOT FOUND"
                ws.write(i, 1, number, red)

            ws.write(i, 2, name)
            ws.write(i, 3, degree)

            if version in list(string.ascii_uppercase[:number_of_versions]):
                ws.write(i, 4, version)
            else:
                error_counter += 1
                ws.write(i, 4, "ERR", red)
            
            for j, t in enumerate(answers, start=5):
                if t not in list(string.ascii_uppercase[:number_of_answers]):
                    warning_counter += 1
                    ws.write(i, j, "", yellow)
                else:
                    ws.write(i, j, t)

            for column, width in enumerate([3000,2000,12000,3000,2000] + [1150] * number_of_questions):
                ws.col(column).width = width

    wb.save("output/reading_results.xls")

    print('Reading complete. Check output/reading_results.xls.')
    if error_counter > 0:
        print(f'\u001b[31;1m{error_counter} errors (student number or version not found)\u001b[0m')
    if warning_counter > 0:
        print(f'\u001b[33;1m{warning_counter} warnings (question unanswered or multiple answers)\u001b[0m')

    if error_counter + warning_counter > 0:
        print('Fix these issues manualy in output/reading_results.xls before grading.')
if __name__ == '__main__':
    reader(10,6, 5)
