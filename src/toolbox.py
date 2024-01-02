import glob
import xlrd
import xlwt
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
    for row, (input_file, number, version) in enumerate(zip(ws.col_values(0,1), ws.col_values(1,1), ws.col_values(4,1)), start=1):
        answers = ws.row_values(row, 5, 5 + number_of_questions)
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
    for number, email, name, degree in zip(ws.col_slice(1,1), ws.col_slice(3,1), ws.col_slice(2,1), ws.col_slice(9,1)):
        short_degree = re.search("-\s(\w*)\s", degree.value).group(1)
        student_list[str(int(number.value))] = (email.value, name.value, short_degree)
    return student_list

# Excel Styles
red = xlwt.easyxf('pattern: pattern solid, fore_colour red;', num_format_str='@')
yellow = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;', num_format_str='@')
red_center = xlwt.easyxf('pattern: pattern solid, fore_colour red; align: horiz center;', num_format_str='@')
green_center = xlwt.easyxf('pattern: pattern solid, fore_colour bright_green; align: horiz center;', num_format_str='@')
header_style = xlwt.easyxf('pattern: pattern solid, fore_colour gray25; align: horiz center; font: bold on;', num_format_str='@')
right_aligned = xlwt.easyxf("align: horiz right;", num_format_str='@')
text_style = xlwt.easyxf(num_format_str='@')
center = xlwt.easyxf('align: horiz center;', num_format_str='@')
integer_style = xlwt.easyxf(num_format_str='0')
grade_style = xlwt.easyxf('font: bold on; align: horiz center;', num_format_str='0.0')