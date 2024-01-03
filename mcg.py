"""
Multiple Choice Grader

author: Simão Leal (simao.leal@tecnico.ulisboa.pt)
"""

import click
import json
import string
import src.bubble_sheet_generator as bbl
import src.reader as rdr
import src.grader as grdr
import src.sender as sndr

def standardize_config(config):
    if list(config.keys()) != ["exam_name", "exam_date", "number_of_questions", 
                       "options_per_question", "number_of_versions", "answer_keys"]:
        raise Exception('Bad config: wrong dictionary keys')
    if type(config["exam_name"]) != str:
        raise Exception('Bad config: type of exam_name should be str')
    if type(config["exam_date"]) != str:
        raise Exception('Bad config: type of exam_date should be str')
    if type(config["number_of_questions"]) != int:
        raise Exception('Bad config: type of number_of_question should be int')
    if config["number_of_questions"] > 60:
        raise Exception('Bad config: Maximum number of questions is 60.')
    if type(config["options_per_question"]) != int:
        raise Exception('Bad config: type of options_per_question should be int')
    if config["options_per_question"] > 6:
        raise Exception('Bad config: Maximum number of options per question is 6.')
    if type(config["number_of_versions"]) != int:
        raise Exception('Bad config: type of number_of_versions should be int')
    if config["number_of_versions"] > 6:
        raise Exception('Bad config: Maximum number of versions is 6.')
    
    if list(map(lambda x: x.capitalize(), config['answer_keys'])) != list(string.ascii_uppercase[:config['number_of_versions']]):
        raise Exception(f'Bad config: wrong number of versions in answer_keys. Versions should be between A and {string.ascii_uppercase[config["number_of_versions"] - 1]}.')
    
    new_answer_keys = dict()
    for key in config['answer_keys']:
        new_answer_keys[key.capitalize()] = [c.capitalize() for c in config['answer_keys'][key]]
        if len(new_answer_keys[key.capitalize()]) != config["number_of_questions"]:
            raise Exception(f'Bad config: wrong number of answers in answer key for version {key.capitalize()}.')
        if any(map(lambda x: x not in string.ascii_uppercase[:config["options_per_question"]], new_answer_keys[key.capitalize()])):
            raise Exception(f'Bad config: bad answers in answer key for version {key.capitalize()}. Answers should be between A and {string.ascii_uppercase[config["options_per_question"] - 1]}.')
        
    config['answer_keys'] = new_answer_keys


@click.group()
def mcg():
    global config
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    standardize_config(config)
    

@mcg.command()
def bubbles():
    bbl.bubbles(config['number_of_questions'], config['options_per_question'], config['number_of_versions'])

@mcg.command()
def reader():
    rdr.reader(config['number_of_questions'], config['options_per_question'], config['number_of_versions'])
    

@mcg.command()
def grader():
    grdr.grader(config['exam_name'], config['exam_date'], config['number_of_versions'],
                 config['number_of_questions'], config['answer_keys'])

@mcg.command()
def sender():
    sndr.sender()

if __name__ == '__main__':
    mcg()