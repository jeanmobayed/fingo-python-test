#!/usr/bin/env python
#coding=utf-8

import os

class FileHandler:
    input_file = ""
    output_file = ""

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def read_file(self):
        """
            separates the input accordingly:
            ref_words: glob is I
            price_msgs: glob glob Silver is 34 Credits
            questions: how much is pish tegj glob glob ?
            error_msgs: not understandable msgs
        """
        ref_words=[]
        price_msgs=[]
        questions=[]
        error_msgs=[]

        info={'ref_words':ref_words,'price_msgs':price_msgs,'questions':questions, 'error_msgs':error_msgs}

        with open(self.input_file) as f:
            for line in f:
                # separate msgs into ref_words, price_msgs and questions
                msg = line.strip()
                # for test
                split_msg = msg.split()
                if split_msg[-1] == '?':
                    questions.append(msg)
                elif split_msg[-1] == 'Credits' and 'is' in msg:
                    price_msgs.append(msg)
                elif split_msg[-1] in 'IVXLCDM' and 'is' in msg:
                    ref_words.append(msg)
                else:
                    error_msgs.append(msg)

        return info

    def write_file(self, result, error_msgs):
        with open(self.output_file, 'w') as f:
            if result:
                f.write('\n'.join(result))
            if error_msgs:
                f.write("\n".join(error_msgs))

    def error_output(self, message):
        with open(self.output_file, 'w') as f:
            if message:
                f.write(message)
