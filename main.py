import re


def apply_operation(operator, left, right):
    answer = left
    if operator == '(':
        return NotImplemented
    elif operator == ')':
        return NotImplemented
    elif operator == '^':
        return NotImplemented
    elif operator == '*':
        answer *= int(right)
    elif operator == '/':
        answer /= int(right)
    elif operator == '+':
        answer += int(right)
    elif operator == '-':
        answer -= int(right)
    else:
        print("Error. Only '+', '-', '*' and '/' are allowed at the moment.")
        exit()
    return answer


def calculator(equation):
    # replace variables with numbers
    letters_indices = [m.span() for m in re.finditer("[a-zA-Z]+", equation)]
    for letIndex in letters_indices:
        key = equation[letIndex[0]:letIndex[1]]
        if key in variables.keys():
            equation = equation.replace(key, variables[key], 1)
        else:
            print("Unknown variable")
            break
    # finding initial and last indexes of numbers, saving in tuples
    else:
        num_indices = [m.span() for m in re.finditer("\d+", equation)]
        prev_number = 0
        prev_end = ''

        for numIndex in num_indices:
            number = float(equation[numIndex[0]:numIndex[1]])

            # If at the start, just add the number
            if numIndex[0] == 0:
                prev_number = number
                prev_end = numIndex[1]
                continue

            # Starting at the second spot of the equation is special
            if numIndex[0] == 1:
                if equation[0] == "(":
                    return NotImplemented
                # It's a negative number
                elif equation[0] == "-":
                    prev_number -= number
                    prev_end = numIndex[1]
                    continue
                else:
                    print("Error. Only numbers, '-' and '(' are allowed at the beginning of the equation.")
                    exit(1)

            # choosing a characters between numbers
            operators = ""
            for o in equation[int(prev_end):].strip():
                if o in ["+", "-", "*", "/"]:
                    operators += o
                else:
                    break
            # replace "--" with "+"
            if "--" in operators and len(operators) % 2 == 0:
                operators = "+"
            # if there are several characters, select the first
            else:
                operators = operators[0]

            # both numbers are positive
            if len(operators) == 1:
                prev_number = apply_operation(operators[0], prev_number, number)
            # if second number is negative
            elif len(operators) == 2:
                if operators[1] == '-':
                    prev_number = apply_operation(operators[0], prev_number, -number)
                else:
                    print("Error. Currently, the second operator must always be a '-'.")
                    exit(1)

            prev_end = numIndex[1]

        # answer
        print(int(prev_number))


def main():
    global variables
    variables = {}
    while True:
        equation = input()

        if len(equation) == 0:
            pass

        elif equation.startswith("/"):
            if equation == "/exit":
                print("Bye!")
                break
            elif equation == "/help":
                print("The program calculates the sum and difference of numbers")
            else:
                print("Unknown command")

        elif "=" not in equation:
            calculator(equation)

        else:
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
                        if value.isnumeric() or value in variables.keys():
                            if value in variables.keys():
                                value = variables[value]
                            variables[key] = value
                        else:
                            print("Invalid assignment")
                    else:
                        print("Invalid identifier")


if __name__ == "__main__":
    main()
