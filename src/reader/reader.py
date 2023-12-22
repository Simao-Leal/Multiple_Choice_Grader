import glob
import os
import csv
import xlwt
import xlrd
import string

# Create a styles
red = xlwt.easyxf('pattern: pattern solid, fore_colour red;')
yellow = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')
header_style = xlwt.easyxf('pattern: pattern solid, fore_colour gray25; font: bold on')
right_aligned = xlwt.easyxf("align: horiz right;")

def remove_left_zeros(number):
    if number == "":
        return ""
    else: 
        return str(int(number))

def reader(number_of_questions, number_of_versions, number_of_answers):
    #extracting student list
    files = glob.glob('input/*.xls')
    if len(files) == 0:
        raise Exception("No .xls file found")
    elif len(files) > 1:
        raise Exception("Multiple .xls files found")  
    else:
        student_list_file = files[0]
    student_list = dict()
    wb = xlrd.open_workbook(student_list_file)
    ws = wb.sheet_by_index(0)
    for number, ist_id, name in zip(ws.col_slice(1,1), ws.col_slice(0,1), ws.col_slice(2,1)):
        student_list[str(int(number.value))] = (ist_id.value, name.value)

    #OMR analysis 
    os.system("rm -r output/*")
    os.system("python3 src/OMRChecker-master/main.py --inputDir OMR_input --outputDir output")
    os.system("mv output/input output/OMR_output")

    #writing results to excel
    file = glob.glob('output/OMR_output/Results/Results*.csv')[0]
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Results')
    header = ["Input File", "IST-ID", "Number", "Name (from student list)", "Version"] + [f"q{i}" for i in range(1, number_of_questions + 1)]
    for i, t in enumerate(header):
        ws.write(0, i, t, header_style)

    with open(file, mode='r') as csvfile:
        results = csv.reader(csvfile)
        already_read = []

        next(results)

        error_counter = 0
        warning_counter = 0

        for i, line in enumerate(results, start=1):
            input_file, _, _, _, version, number, *answers = line

            ws.write(i, 0, input_file, right_aligned)

            number = remove_left_zeros(number)

            if number in student_list:
                if number not in already_read:
                    ist_id, name = student_list[number]
                    ws.write(i, 1, ist_id)
                    ws.write(i, 2, number)
                    ws.write(i, 3, name)
                    already_read.append(number)
                else:
                    error_counter += 1
                    ist_id, name = "DUPLICATE", "THIS STUDENT NUMBER WAS SEEN TWICE"
                    ws.write(i, 1, ist_id)
                    ws.write(i, 2, number, red)
                    ws.write(i, 3, name)
            else:
                error_counter += 1
                ist_id, name = "NOT FOUND", "STUDENT NUMBER NOT FOUND IN STUDENT LIST"
                ws.write(i, 1, ist_id)
                ws.write(i, 2, number, red)
                ws.write(i, 3, name)

            if version in string.ascii_uppercase[:number_of_versions]:
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

            for column, width in enumerate([3000,3000,2000,12000,2000] + [1000] * number_of_questions):
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
