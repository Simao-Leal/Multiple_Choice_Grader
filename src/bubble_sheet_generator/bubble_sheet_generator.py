#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import string
import json
import os
import fitz
import tempfile
import random

def answer_sheet_maker(number_of_questions, number_of_answers, number_of_versions, print_version = None, answer_key = None, file_name = 'reference'):

    questions_per_column = \
        [number_of_questions // 4 for _ in range(4 - number_of_questions % 4)] + \
        [number_of_questions // 4 + 1 for _ in range(number_of_questions % 4)]

    
    file =r"""
    \documentclass[a4paper]{article}
    \usepackage{tikz}
    \usetikzlibrary{calc}
    \usepackage{subfig}
    \usepackage[a4paper, top=2cm, bottom=2cm, left=2cm, right=2cm]{geometry}
    \usepackage{amssymb}
    \usepackage{eso-pic}
    \pagestyle{empty}
    
    \newcommand{\radius}{6pt}
    \setlength{\parindent}{0pt}
    \begin{document}

    \begin{minipage}[c][4.5cm][c]{\textwidth}
    """
    with open("header.tex", "r") as f:
        file += f.read()
    file += r"""
    \end{minipage}
    \vspace{10pt}
    {\Large\textbf{Número de Aluno:}}
    \begin{tikzpicture}[baseline = -0.2cm]
    	\foreach \column in {1,2,...,6} {
    		\begin{scope}[xshift= 7*\column mm]
    			\node[rectangle, draw, minimum width=5mm, minimum height=6mm] at (0,0) {};
    			\foreach \number in {0,1,...,9} { 
    				\draw (0, {-(0.1 + (\number + 1) * 0.55)}) circle[radius=\radius] node {\number};
    			}
    		\end{scope}
    	}
    \end{tikzpicture}
    \hfill
    {\Large\textbf{Versão:}}
    """
    
    file += r"\begin{tikzpicture}[baseline = -5pt]" + "\n"
    for i, version in enumerate(string.ascii_uppercase[:number_of_versions]):
        file += r"\draw " +("[fill=black]" if version == print_version else "") + \
            f" ({round(i * 0.7, 2)}, 0)" + \
            r" circle[radius=\radius" + \
            "] node {" + version + "};\n"
    file += r"\end{tikzpicture}" + "\n"
    
    file += r"""
    \bigskip
    \begin{center}
    	\Large \textbf{Folha de Respostas}
    \end{center}
    """
    
    file += r"\begin{tikzpicture}[remember picture, overlay, xshift = -4.1cm, yshift = 0.1cm]" + "\n"
    questions_placed = 0
    for column, questions_to_place in enumerate(questions_per_column, start = 1):
        for i,label in zip(range(questions_to_place), range(questions_placed + 1, questions_placed + questions_to_place + 1)):
            y = str(round(-i*0.9,2))
            xstart = column * 4.38 
            file += r"\node at (" + str(round(xstart,2)) + ", " + y +r") {\textbf{" + str(label) + "}};"+"\n"
            for j,letter in zip([1,2,3,4,5,6],['A','B','C','D','E','F']):
                x = str(round(xstart + j * 0.55,2))
                if j <= number_of_answers:
                    file += r"\draw" + ("[fill=black]" if answer_key != None \
                                        and letter in answer_key[questions_placed] else "") + \
                    " (" + x + ", " + str(y) + r") circle[radius=\radius]  node {" + str(letter) + "};" + "\n"
        
            questions_placed += 1
    
    file += r"\end{tikzpicture}" + "\n"        
    file += r"\end{document}"
    
    
    #saving files
    
    with tempfile.TemporaryDirectory() as directory:
        with open(f"{directory}/bubble_sheet.tex", "w") as f:
            f.write(file)
            
        os.system(f"cp {directory}/bubble_sheet.tex /Users/simaoleal/Desktop/idk.tex")
        
        os.system(f"pdflatex -output-directory={directory} --interaction=batchmode {directory}/bubble_sheet.tex")
        
        if(print_version != None or answer_key != None):
            os.system(f"cp {directory}/bubble_sheet.pdf answer_sheets/{file_name}.pdf")
            
        else:
            doc = fitz.open(f'{directory}/bubble_sheet.pdf')
            page = doc[0]
            mat = fitz.Matrix(2.08, 2.08)
            pixmap = page.get_pixmap(matrix = mat)
            pixmap.save("OMR_input/reference.png")
            
            
            
def template_maker(number_of_questions, number_of_answers, number_of_versions):
    
    template = {
    "pageDimensions": [ 900, 1312 ],
    "bubbleDimensions": [ 22, 22 ],
    "customLabels": {
        "id": ["id1..6"]
       },
      "preProcessors": [
      	{
          "name": "FeatureBasedAlignment",
          "options": {
            "reference": "reference.png",
            "maxFeatures": 1000,
            "2d": True
          }
        },
        {
            "name": "Levels",
            "options": {
              "low": 0.5
            }
        }
      ],
      
    "fieldBlocks": {
        "NumeroIST": {
      	  "fieldType": "QTYPE_INT",
          "fieldLabels": [
              "id1..6"
          ],
          "bubblesGap": 24.2,
          "labelsGap": 30,
          "origin": [
            291,
            320
          ]
      	},
        
        "Version": {
          "origin": [
            793 - 30 * (number_of_versions - 1),
            292
          ],
          "direction": "horizontal",
          "bubblesGap": 30,
          "bubbleValues": [x for x in string.ascii_uppercase[:number_of_versions]], 
          "fieldLabels": ["Version"],
          "labelsGap": 0
        },
      }
    }
    
    MQBorigins = [[110,645], [298, 645], [486,645], [674,645]]
    questions_per_column = \
        [number_of_questions // 4 for _ in range(4 - number_of_questions % 4)] + \
        [number_of_questions // 4 + 1 for _ in range(number_of_questions % 4)]
        
    questions_placed = 0
    for column, (questions_to_place, origin) in enumerate(zip(questions_per_column, MQBorigins), start = 1):
        template["fieldBlocks"][f"MCQ_Block_{column}"] = {
                "origin": origin,
                "direction": "horizontal",
                "bubblesGap": 23.4,
                "bubbleValues": ["A", "B", "C", "D", "E", "F"][:number_of_answers], 
                "fieldLabels": [f"q{i}" for i in range(questions_placed + 1, questions_placed + questions_to_place + 1)],
                "labelsGap": 39.7
            }
        questions_placed += questions_to_place
        
    # saving files
    with open("OMR_input/template.json", "w") as f:
            json.dump(template, f)
        
        
if __name__ == '__main__':
    template_maker(10, 5, 6)
    w = ['A', 'B', 'C', 'D', 'E', 'F']

    for version in w:
        answer_sheet_maker(10, 5, 6, print_version = version, file_name = f"test_version_{version}")
    