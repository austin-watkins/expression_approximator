from sympy import *
from random import randint, seed
from PIL import Image
from os import listdir, makedirs
from os.path import isfile, join


def form_image(content, fix_size=True, path='unprocessed/', top_right=True):
    """
    Given a string (content) creates a picture that has that expression (evaluated in LaTex).
    """
    assert isinstance(content, str)

    preamble = "\\documentclass{article} \n\
                \\usepackage[paperheight=80px, paperwidth=110px]{geometry} \
                \\pagenumbering{gobble} \
                \\begin{document}\\"

    file_name = content
    makedirs(path, exist_ok=True)
    if top_right:
        latex = 'I\\texttt{' + content + '}\\\\I'
        preview(latex, output='png', viewer='file', filename=f'{path}{file_name}.png')
    else:
        latex = '\\texttt{' + content + '}\\\\AAAAA'
        preview(latex, output='png', viewer='file', filename=f'{path}{file_name}.png')


def random_number(largest_possible_value=1000):
    number = randint(0, largest_possible_value)
    expression = str(number)
    return expression, number

def random_addition(largest_possible_value=1000):
    """
    Given the largest possible value.
    Generates a random addition expression and the value that it would be if evaluated.
    Note that the largest size is inclusive.
    """
    # fixme figure out how to get the largest size
    possible_size = len(str(largest_possible_value))

    # Generate integers.
    first_operand = randint(0, largest_possible_value)
    second_operand = randint(0, largest_possible_value)

    # Get expression
    first_equation_str = str(first_operand).rjust(6)
    second_equation_str = str(second_operand).rjust(6)
    equation_list = list(first_equation_str) + ['+'] + list(second_equation_str)
    joined_equation = ' & '.join(equation_list)

    # Get answer.
    result = first_operand + second_operand

    # # form string representation.
    # first_operand = str(first_operand)
    # second_operand = str(second_operand)
    # first_operand = '0' * (possible_size - len(first_operand)) + first_operand
    # second_operand = '0' * (possible_size - len(second_operand)) + second_operand
    #
    # expression = f'{first_operand} + {second_operand}'

    tabular_format1 = '''\\begin{tabular}{p{0.05cm} p{0.05cm} p{0.05cm} p{0.05cm} p{0.05cm} p{0.05cm}
    p{0.05cm}
    p{0.05cm} p{0.05cm} p{0.05cm} p{0.05cm} p{0.05cm} p{0.05cm}}\n'''
    tabular_format2 = '\n\\end{tabular}'

    expression = tabular_format1 + joined_equation + tabular_format2
    return expression, result

def helper(x):
    return  form_image(x, path='test/', top_right=False)

def multi_threaded_printing(expressions):
    """
    Prints out expressions using as many cores as the CPU has.
    """
    from multiprocessing import cpu_count, Pool

    try:
        iter(expressions)
    except TypeError:
        raise TypeError('expressions must be iterable.')
    cores = cpu_count()
    pool = Pool(processes=cores)


    pool.map(helper, expressions)


def trip_expression(expressions_path, destination_folder):
    makedirs(destination_folder, exist_ok=True)
    makedirs(expressions_path, exist_ok=True)
    files = [f for f in listdir(expressions_path) if isfile(join(expressions_path, f))]
    for f in files:
        img = Image.open(expressions_path + '/' + f)
        width, height = img.size
        #img = img.crop((width - 110, 1, width, 10))
        img = img.crop((0, 0, 54, 13))
        img = img.convert('L')
        img.save(f'{destination_folder}/{f}')


def generate_random_number_files(digit_generation):
    expressions = set()
    expressions_len = 0

    min = 0
    max = 9

    for digit_len in digit_generation:
        expressions_len += digit_generation[digit_len]
        while len(expressions) < expressions_len:
            rand_num = randint(min, max)
            expressions.add(str(rand_num))

        min = 10 ** (digit_len)
        max = (min * 9) + max

    import time

    t0 = time.time()
    multi_threaded_printing(expressions)
    delta = time.time() - t0

    trip_expression('test/', 'random_numbers/')


if __name__ == '__main__':
    digit_generation = {1: 5,
                        2: 50,
                        3: 500,
                        4: 5000,
                        5: 20000,
                        6: 20000}
    generate_random_number_files(digit_generation)
    exit()

    seed(42)
    expressions = set()
    number_of_expressions = 100
    while len(expressions) < number_of_expressions:
        question, answer = random_number(999999)
        expressions.update([question])

    import time

    t0 = time.time()
    multi_threaded_printing(expressions)
    delta = time.time() - t0
    print(f'Printing took:\n'
          f'\tTOTAL\t{delta:.3} seconds \n'
          f'\tAVERAGE\t{number_of_expressions/ delta :.4} exp/second')
    trip_expression('test/', 'random_numbers/')
