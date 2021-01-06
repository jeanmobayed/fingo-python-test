#!/usr/bin/env python
#coding=utf-8

import sys
import os

from input_parser import InputParser
from file_handler import FileHandler

DEFAULT_ANSWER = "I have no idea what you are talking about"

def start_process(input_file, output_file):
    handler = FileHandler(input_file, output_file)

    info = handler.read_file()
    error_msgs = info['error_msgs']
    
    if len(info['ref_words']) > 0:
        parser = InputParser(DEFAULT_ANSWER)

        result = parser.process_info(info['ref_words'], info['price_msgs'])
        if result:
            error_msgs.extend(result)

        answers = parser.answer_questions(info['questions'])

        handler.write_file(answers, error_msgs)

    else:
        handler.error_output("No correct inputs found.")

if __name__ == '__main__':
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.txt'

    if not os.path.isfile(input_file):
        handler = FileHandler('', output_file)
        handler.error_output("Can't find the input file: " + input_file)
        exit(1)

    start_process(input_file, output_file)