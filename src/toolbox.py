import glob
import xlrd
import re

def remove_left_zeros(number):
    if number == "":
        return ""
    else: 
        return str(int(number))
    
def get_reading_results(number_of_questions):
    reading_results = dict()
    wb = xlrd.open_workbook("output/reading_results.xls")
    ws = wb.sheet_by_index(0)
    for row, (input_file, number, version) in enumerate(zip(ws.col_values(0,1), ws.col_values(2,1), ws.col_values(5,1)), start=1):
        answers = ws.row_values(row, 6, 6 + number_of_questions)
        reading_results[number] = (input_file, version, answers)
    return reading_results

def get_student_list():    
    #extracting student list
    files = glob.glob('input/*.xls')
    if len(files) == 0:
        raise Exception("No .xls student list found")
    elif len(files) > 1:
        raise Exception("Multiple .xls student lists found")  
    else:
        student_list_file = files[0]
    student_list = dict()
    wb = xlrd.open_workbook(student_list_file)
    ws = wb.sheet_by_index(0)
    for number, ist_id, name, degree in zip(ws.col_slice(1,1), ws.col_slice(0,1), ws.col_slice(2,1), ws.col_slice(9,1)):
        short_degree = re.search("-\s(\w*)\s", degree.value).group(1)
        student_list[str(int(number.value))] = (ist_id.value, name.value, short_degree)
    return student_list