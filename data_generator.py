from sympy import *
from random import randint
from PIL import Image
from os import listdir
from os.path import isfile,join



def form_image(content, fix_size=True, path='data2/'):
    """
    Given a string (content) creates a picture that has that expression (evaluated in LaTex).
    """
    assert isinstance(content, str)

    preamble = "\\documentclass{article} \n\
                \\usepackage[paperheight=80px, paperwidth=110px]{geometry} \
                \\pagenumbering{gobble} \
                \\begin{document}\\"

    file_name = content
    if fix_size:
        # latex = '.  \\scalebox{1.2}{$' + content + '$}.'
        latex = 'I\\texttt{' + content + '}\\\\I'
        yield preview(latex, output='png', viewer='file', filename=f'{path}{file_name}.png', preamble=preamble)
    else:
        latex = f'${content}$'
        yield preview(latex, output='png', viewer='file', filename=f'{path}{file_name}.png')


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

    # Get answer.
    result = first_operand + second_operand

    # form string representation.
    first_operand = str(first_operand)
    second_operand = str(second_operand)
    first_operand = '0' * (possible_size - len(first_operand)) + first_operand
    second_operand = '0' * (possible_size - len(second_operand)) + second_operand

    expression = f'{first_operand} + {second_operand}'
    return expression, result


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
    pool.map(form_image, expressions)


def trip_expression(expressions_path, destination_folder):
    files = [f for f in listdir(expressions_path) if isfile(join(expressions_path, f))]
    for f in files:
        img = Image.open(expressions_path + '/' + f)
        width, height = img.size
        img = img.crop((width - 107, 1, width, 10))
        img.save(f'{destination_folder}/{f}')

if __name__ == '__main__':
    trip_expression('data2', 'processed')
    exit()
    expressions = set()
    number_of_expressions = 1
    while len(expressions) < number_of_expressions:
        question, answer = random_addition(999999)
        expressions.update([question])

    import time

    t0 = time.time()
    multi_threaded_printing(expressions)
    delta = time.time() - t0
    print(f'Printing took:\n'
          f'\tTOTAL\t{delta:.3} seconds \n'
          f'\tAVERAGE\t{number_of_expressions/ delta :.4} exp/second')
