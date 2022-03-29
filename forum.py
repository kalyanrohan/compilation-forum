import re
from numpy import source
#php lexical analyzer

tokens=[]


# token class 
token_dict = {
    '+' : 'addition-sign',
    '-' : 'minus',
    '=' : 'assignment',
    '*' : 'multiply',
    '/' : 'divide',
    ';' : 'semi-colon',
    '(' : 'open-bracket',
    ')' : 'close-bracket',
    '{' : 'open-bracket-curl',
    '}' : 'close-bracket-curl',
    '=='   : 'equal',
    '==='  : 'identical',
    '.'    :'string-concat',
    '//'   :'single-line',
    '#' :'single-comment',
    '/*':'multi-line-comment',
    '*/':'close-multi-comment',
    '$' : 'variable',
    ' ' :'space',
}

#keywords 
identifier_dict = {
    'echo' : 'print-output',
    'function' :'function',
    'class' : 'class',
    '<?php' : 'php-opening-tag',
    '?>' : 'php-closing-tag',
}

# Read file
lines = []
with open('source.php') as f:
    for line in f:
        lines.append(line.strip())

# Scanning
output = []

def output_line(line_number, column, token_class, token_value = None):
    return f'{line_number},{column},{token_class}' if token_value == None else f'{line_number},{column},{token_class},{token_value}'

for line_num in range(lines):
    line = lines[line_num]
    split_words = line.split()

    #starts from column 1 
    column = 1
    
    #to check if it is the name of the function or class
    is_class = False
    is_function = False
    is_echo = False
    is_php_opening_tag = False
    is_php_closing_tag = False
    is_single_line_comment = False
    is_multi_line_comment = False
    is_string_concat = False
    
    for word in split_words:
        if word == '<?php':
            is_php_opening_tag = True
            output.append(output_line(line_num, column, token_dict['<?php']))
        elif word == '?>':
            is_php_closing_tag = True
            output.append(output_line(line_num, column, token_dict['?>']))
        elif word == 'class':
            is_class = True
            output.append(output_line(line_num, column, token_dict['class']))
        elif word == 'function':
            is_function = True
            output.append(output_line(line_num, column, token_dict['function']))
        elif word == 'echo':
            is_echo = True
            output.append(output_line(line_num, column, token_dict['echo']))
        elif word == '//':
            is_single_line_comment = True
            output.append(output_line(line_num, column, token_dict['//']))
        elif word == '/*':
            is_multi_line_comment = True
            output.append(output_line(line_num, column, token_dict['/*']))
        elif word == '*/':
            is_multi_line_comment = False
            output.append(output_line(line_num, column, token_dict['*/']))
        elif word == '.':
            is_string_concat = True
            output.append(output_line(line_num, column, token_dict['.']))
        elif word == '==':
            output.append(output_line(line_num, column, token_dict['==']))
        
        if is_function:
            if word in identifier_dict:
                output.append(output_line(line_num, column, identifier_dict[word]))
            else:
                output.append(output_line(line_num, column, token_dict['$'], word))
        

