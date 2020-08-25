import re


def applyOperation(operator, left, right):
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
    pass

def main():
    global index, operators
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
            lettersIndices = [m.span() for m in re.finditer("[a-zA-Z]+", equation)]
            for letIndex in lettersIndices:
                key = equation[letIndex[0]:letIndex[1]]
                if key in variables.keys():
                    equation = equation.replace(key, variables[key], 1)
                else:
                    print("Unknown variable")
                    break
            else:
                numIndices = [m.span() for m in re.finditer("\d+", equation)]
                prevNumber = 0
                prevEnd = ''

                for numIndex in numIndices:
                    number = float(equation[numIndex[0]:numIndex[1]])

                    # If at the start, just add the number
                    if numIndex[0] == 0:
                        prevNumber = number
                        prevEnd = numIndex[1]
                        continue

                    # Starting at the second spot of the equation is special
                    if numIndex[0] == 1:
                        # Remember this for order of operations (if implemented)
                        if equation[0] == "(":
                            # I think handling these would be best done recursively
                            # Or you could split on all parentheses and compute each in turn
                            # Or ...
                            return NotImplemented
                        # It's a negative number
                        elif equation[0] == "-":
                            prevNumber -= number
                            prevEnd = numIndex[1]
                            continue
                        else:
                            print("Error. Only numbers, '-' and '(' are allowed at the "
                                  + "beginning of the equation.")
                            # You could allow a period as well.
                            exit(1)

                    # If reached here, then should have passed the first number
                    # Extract relevant operators and remove any spaces
                    operators = ""
                    for o in equation[int(prevEnd):].strip():
                        if o in ["+", "-"]:
                            operators += o
                        else:
                            break

                    if "--" in operators and len(operators) % 2 == 0:
                        operators = "+"
                    else:
                        operators = operators[0]

                    # operators = equation[prevEnd:numIndex[0]]
                    # operators = "".join(operators.split())

                    if len(operators) == 1:
                        prevNumber = applyOperation(operators[0], prevNumber, number)

                    elif len(operators) == 2:
                        if (operators[1] == '-'):
                            prevNumber = applyOperation(operators[0], prevNumber, -number)
                        else:
                            print("Error. Currently, the second operator must always be a '-'.")
                            exit(1)

                    # If it reaches here, then parentheses are probably involved
                    # or syntax is probably incorrect
                    else:
                        print("Error. Only two operators are currently allowed between numbers."
                              + " The second one always being a '-'.")
                        # You could allow all sorts of nesting with parentheses if you want.
                        exit(1)
                    prevEnd = numIndex[1]

                    # Do not display the decimal places if they are all 0
                prevNumber = int(prevNumber) if prevNumber - int(prevNumber) == 0 else prevNumber
                # answer
                print(prevNumber)

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
