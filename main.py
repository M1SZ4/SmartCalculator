import re
from collections import deque


def assign_variable(equation):
    """Assign value to variable or change value of existing variable"""
    if equation.count("=") > 1:
        print("Invalid assignment")

    else:
        try:
            index = equation.index("=")
        except ValueError:
            print("Invalid assignment")
        else:
            key = equation[:index].strip()
            value = equation[index + 1:].strip()
            if key.isalpha():
                if is_number(value) or value in variables.keys():
                    if value in variables.keys():
                        value = variables[value]
                    variables[key] = value
                else:
                    print("Invalid assignment")
            else:
                print("Invalid identifier")


def is_number(string):
    """Return true if variable can be converted to integer"""
    try:
        int(string)
        return True
    except ValueError:
        return False


def tokenize_input(input_string):
    """Replace multiple "+" or "-", split each element in a list"""
    # delete whitespaces
    input_string = re.sub(r"\s+", "", input_string)
    # replace multiple + with a single one
    input_string = re.sub("\+\++", "+", input_string)
    # replace odd number of "-" with a sigle one
    input_string = re.sub("---", "-", input_string)
    # replace even number of "-" with a sigle one
    input_string = re.sub("--+", "+", input_string)

    result = []

    while input_string:
        # search for numbers
        if input_string[0].isnumeric():
            number = input_string[0]
            input_string = input_string[1:]
            while input_string and input_string[0].isnumeric():
                number += input_string[0]
                input_string = input_string[1:]
            result.append(number)
        # search for variables
        elif input_string[0].isalpha():
            variable = input_string[0]
            input_string = input_string[1:]
            while input_string and input_string[0].isalpha():
                variable += input_string[0]
                input_string = input_string[1:]
            result.append(variable)
        elif input_string[0] in ["+", "-", "/", "*", "(", ")", "^"]:
            # more than one mark - error
            try:
                if input_string[1] in ["/", "*", "^"]:
                    print("Invalid expression")
                    return False
            except IndexError:
                pass
            result.append(input_string[0])
            input_string = input_string[1:]

    return result


def replace_variables(user_input):
    """
    Replace variables with value or print error if variable is not existing
    Check if expression is no too short, and all parentheses are closed
    """
    result = []

    for token in user_input:
        if token.isalpha():
            if token in variables.keys():
                result.append(variables[token])
            else:
                print("Unknown variable")
                return False
        else:
            result.append(token)
    # if expression is too short
    if len(result) < 2:
        print("Invalid expression")
        return False
    # if the parentheses do not match
    elif result.count('(') != result.count(')'):
        print("Invalid expression")
        return False

    return result


def infix_to_postfix(input_values):
    """return postfix notation, including negative numbers"""
    precedence = {
        "neg": 1,
        "(": 1,
        "-": 2,
        "+": 2,
        "/": 3,
        "*": 3,
        "^": 3,
    }
    stack = deque()
    postfix_result = list()

    unary = True
    neg = False

    for token in input_values:
        if unary and token in "+-":
            if token == "-":
                neg = not neg
        elif is_number(token):
            if neg:
                postfix_result.append(int("-" + token))
            else:
                postfix_result.append(int(token))
            neg = False
            unary = False
        elif token == '(':
            if neg:
                stack.append("neg")
                neg = False
            stack.append(token)
            unary = True
        elif token == ')':
            top_element = stack.pop()
            unary = False
            while top_element != '(':
                postfix_result.append(top_element)
                top_element = stack.pop()
            if len(stack) != 0 and stack[-1] == "neg":
                postfix_result.append(stack.pop())
        else:
            while (len(stack) != 0) and (precedence[stack[-1]] >= precedence[token]):
                postfix_result.append(stack.pop())
            stack.append(token)
            unary = True

    while len(stack) != 0:
        postfix_result.append(stack.pop())

    return postfix_result


def calculate(a, b, operator):
    """return result of one math operation"""
    temp_result = 'Calculation error'
    if operator == '-':
        temp_result = a - b
    elif operator == '+':
        temp_result = a + b
    elif operator == '*':
        temp_result = a * b
    elif operator == '/':
        temp_result = a / b
    elif operator == '^':
        temp_result = a ** b
    return temp_result


def evaluate_expression(expression_stack):
    """calculate all parts of expression, return result"""
    calculation_stack = list()
    for item in expression_stack:
        if isinstance(item, int):
            calculation_stack.append(item)
        elif item in ['+', '-', '*', '/', '^']:
            num_1 = calculation_stack.pop()
            num_2 = calculation_stack.pop()
            calculation_stack.append(calculate(num_2, num_1, item))
    return calculation_stack[-1]


def main():
    global variables
    variables = {}
    while True:
        user_input = input()

        # if the user has not entered anything, ask again for input
        if len(user_input) == 0:
            pass

        # if input starts with "/", follow the command
        elif user_input.startswith("/"):
            if user_input == "/exit":
                print("Bye!")
                break
            elif user_input == "/help":
                print("The calculator supports: addition '+', subtraction '-', multiplication '*', integer division "
                      "'/', exponent '^' and parentheses '(...)'.\n"
                      "Program support positive and negative numbers and also correct order of operations.\n"
                      "If you want to leave type '/exit'\n"
                      "Variables:\n"
                      "\t- Variable name can contain only letters, names are case sensitive\n"
                      "\t- The value can be an integer number or a value of another variable\n"
                      "\t- You can change the value of an existing variable\n"
                      "\t- To print the value of a variable just type its name")
            else:
                print("Unknown command")

        # assign value to variable
        elif "=" in user_input:
            assign_variable(user_input)

        # do math
        else:
            # separate each element of expression into a list
            user_input = tokenize_input(user_input)
            if user_input is False:
                continue

            # if user enter variable name print value of this variable
            if len(user_input) == 1 and user_input[0] in variables.keys():
                print(variables[user_input[0]])
                continue

            # replace variables with values and check if expression is no too short, and all parentheses are closed
            user_input = replace_variables(user_input)
            if user_input is False:
                continue

            # convert to postfix
            postfix_stack = infix_to_postfix(user_input)

            # do math and print result
            print(int(evaluate_expression(postfix_stack)))


if __name__ == "__main__":
    main()
