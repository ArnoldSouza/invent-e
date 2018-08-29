from clint.textui import puts, indent, colored, prompt, validators  # prettify the command line interface
from string import Formatter  # lib to query string to find parameters inside


def extract_keywords(text_sql):
    """
    extract the keyword arguments from a Python format string
    :param text_sql: String of SQL script
    :return: list of parameters
    """
    list_parameters = [fname for _, fname, _, _ in Formatter().parse(text_sql) if fname]
    return list_parameters


def check_parameters(text_sql, dict_answers=None):
    """
    Function to check if a given string has parameters inside
    :param text_sql: string of SQL script
    :param dict_answers: dictonary of answers to the existing parameters in the string
    :return: list of parameters if exists
    """
    list_parameters = extract_keywords(text_sql)

    if not list_parameters:  # if no param, return the given string
        return text_sql
    else:  # ask the user to input data
        if dict_answers:
            return text_sql.format(**dict_answers)  # substitute the parameters inside the string
        else:
            return _get_param(list_parameters, text_sql)  # look for user input


def _get_param(list_parameters, text_sql):
    """
    uses clint lib to ask the user to input data. This fuction assumes no Null arguments

    :param list_parameters: parameters of the SQL String
    :param text_sql: the given SQL String
    :return: the SQL String with the parameters values inside
    """
    length = len(list_parameters)
    puts(colored.yellow(f'Found {length} parameters in the SQL that need input:'))
    with indent(4, quote=colored.blue('>')):
        puts('param: '+colored.blue(f'{list_parameters}'))

    answers = {}
    for param in list_parameters:  # iterate over params to get inputs
        answers[param] = _prompt_param(param)
    text_sql = text_sql.format(**answers)  # substitute the parameters inside the string
    return text_sql


class _InputValidator(object):
    message = 'Input is not valid.'

    def __init__(self, fun, message=None, *args):
        if message is not None:
            self.message = message
        self.my_function = fun
        self.my_args = args

    def __call__(self, value):
        """
        Validates the input.
        """
        try:
            return self.my_function(value, *self.my_args)
        except (TypeError, ValueError):
            raise validators.ValidationError(self.message)


def _greater_than(value, number):
    """
    check if a value satisfy a condition to a number
    :param value: value to be analised, provided by __call__
    :param number: number to compare
    :return: either the value or an error
    """
    if int(value) >= int(number):
        return value
    else:
        raise ValueError


def _prompt_param(param):
    """
    prompt to the user the parameters to input
    :param param: list of parameters
    :return: answer (string)
    """
    if param == 'filial':
        answer = prompt.query(f'Insert subsidiary code ({param}):',
                              '02',
                              validators=[validators.RegexValidator(r"^\d{2}$", 'Value must be two numeric digits')],
                              batch=False)
        answer = f"'{answer}'"  # puts result in single quotes because of SQL interpreter
    elif param == 'armazem':
        answer = prompt.query(f'Insert warehouse code ({param}):',
                              '21',
                              validators=[validators.RegexValidator(r"^\d{2}$", 'Value must be two numeric digits')],
                              batch=False)
        answer = f"'{answer}'"  # puts result in single quotes because of SQL interpreter
    elif param == 'codigo':
        answer = prompt.query(f'Insert product code ({param}):',
                              '02500727',
                              validators=[validators.RegexValidator(r"^\d{8}$", 'Value must be eight numeric digits')],
                              batch=False)
        answer = f"'{answer}'"  # puts result in single quotes because of SQL interpreter
    elif param == 'intervalo':
        answer = prompt.query(f'Insert range ({param}) in days:',
                              '365',
                              validators=[_InputValidator(_greater_than,
                                                          "Must to be greater than 30 days",
                                                          30)],
                              batch=False)
        answer = int(answer)*-1
    else:
        answer = prompt.query(f'[UNKNOWN PARAMETER] Insert a value to -> {param}:')
        answer = f"'{answer}'"  # puts result in single quotes because of SQL interpreter
    return answer
