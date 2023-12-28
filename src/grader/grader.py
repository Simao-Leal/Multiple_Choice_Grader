import tempfile
import os


def evaluation_report_maker(exam_name, exam_date, name, number, ist_id, course, version,
                             answer_key, answers, no_correct, no_incorrect, no_unanswered, grade, path):
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
                             tables=tables, no_correct=no_correct, no_incorrect=no_incorrect, no_unanswered=no_unanswered, grade=grade, path=path)
        print(tex)

    with tempfile.TemporaryDirectory() as directory:
        with open(f"{directory}/evaluation_report.tex", "w") as f:
            f.write(tex)
        
        os.system(f"pdflatex -output-directory={directory} --interaction=batchmode {directory}/evaluation_report.tex")
        os.system("mkdir -p output/evaluation_reports")
        os.system(f"cp {directory}/evaluation_report.pdf output/evaluation_reports/{ist_id}.pdf")
       

if __name__ == '__main__':
    evaluation_report_maker('Exame AMC Época Normal', '31/02/2024, 10:30', 'Simão', '92648', 'ist192648', 'LMAC', 'A', ['A', 'B', 'C', 'D', 'E'] + ['A'] * 39, ['A', 'D', 'E', '', 'A'] + ['A'] * 39, 2, 3, 0, '19,5', '/Users/simaoleal/Desktop/Multiple_Choice_Grader/input/Scanned from a Xerox Multifunction Printer001.jpg')