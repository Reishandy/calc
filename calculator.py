SUPPORTED_OPERATIONS = ["+", "-", "*", "/", "^"]


def calculate(input: str) -> float | int:
    if not input:
        raise SyntaxError(f"Empty equation")

    if input[0] in SUPPORTED_OPERATIONS:
        input = "0" + input

    components = parse(input)

    parentheses_operation(components)
    carat_operation(components)
    higher_operation(components)
    result = lower_operation(components)

    if result.is_integer():
        result = int(result)
    else:
        result = round(result, 5)

    return result


# PARSING
def parse(input_string: str) -> list[int | str]:
    components = list(input_string)

    if len(components) == 0:
        raise SyntaxError(f"Empty equation")

    i = 0
    while i < len(components):
        if i > 0 and type(components[i - 1]) == float and components[i] == "(":
            components.insert(i, "*")

        if is_digit(components[i]):
            digit_buffer = components[i]

            while i + 1 != len(components) and is_digit(components[i + 1]):
                digit_buffer += components[i + 1]
                components.pop(i + 1)

            if digit_buffer.count(".") > 1:
                raise SyntaxError(f"{input_string}")

            components[i] = float(digit_buffer)

        elif components[i] == "(":
            front_pair = 0
            last = i + 1

            for char in components[last:]:
                if char == "(":
                    front_pair += 1

                elif char == ")":
                    if front_pair == 0:
                        break

                    front_pair -= 1

                last += 1

            if last == len(components):
                raise SyntaxError(f"No closing parentheses")

            components[i] = "".join(components[i : last + 1])
            del components[i + 1 : last + 1]

        elif components[i] == ")":
            raise SyntaxError(f"No opening parentheses")

        elif components[i] not in SUPPORTED_OPERATIONS:
            raise SyntaxError(f"Unsupported operation: {components[i]}")

        elif components[i] in SUPPORTED_OPERATIONS:
            if i == len(components) - 1:
                raise SyntaxError(f"Syntax error: {input_string}")
            if components[i - 1] in SUPPORTED_OPERATIONS:
                raise SyntaxError(f"Syntax error: {input_string}")

        i += 1

    return components


# OPERATIONS
def parentheses_operation(components: list[float | str]):
    i = 0

    while i < len(components):
        if type(components[i]) != float and components[i] not in SUPPORTED_OPERATIONS:
            parentheses_component = parse(components[i][1:-1])

            parentheses_operation(parentheses_component)
            carat_operation(parentheses_component)
            higher_operation(parentheses_component)
            result = lower_operation(parentheses_component)

            components[i] = result

        i += 1


def carat_operation(components: list[float | str]):
    i = len(components) - 1

    while i > 0:
        if components[i] == "^":
            components[i] = components[i - 1] ** components[i + 1]
            components.pop(i + 1)
            components.pop(i - 1)
            i -= 1

        i -= 1


def higher_operation(components: list[float | str]):
    i = 0

    while i < len(components):
        if components[i] == "*":
            components[i] = components[i - 1] * components[i + 1]
            components.pop(i + 1)
            components.pop(i - 1)
            i -= 1

        elif components[i] == "/":
            components[i] = components[i - 1] / components[i + 1]
            components.pop(i + 1)
            components.pop(i - 1)
            i -= 1

        i += 1


def lower_operation(components: list[float | str]) -> int:
    result = components[0]

    for i in range(len(components) - 1):
        element = components[i]
        next_element = components[i + 1]

        match element:
            case "+":
                result += next_element
            case "-":
                result -= next_element

    return result


# UTILS
def is_digit(str) -> bool:
    return str.lstrip("-").replace(".", "").isdigit() or str == "."


if __name__ == "__main__":
    print(calculate(""))

    # # Test: Basic Operations
    # print(calculate("1+1"))  # Expected: 2
    # print(calculate("2-1"))  # Expected: 1
    # print(calculate("2*2"))  # Expected: 4
    # print(calculate("10/2"))  # Expected: 5
    # print(calculate("2^3"))  # Expected: 8
    # print()

    # # Test: Order of Operations
    # print(calculate("1+2*3"))  # Expected: 7
    # print()

    # # Test: Parenteses
    # print(calculate("((1))"))  # Expected: 1
    # print(calculate("((1+1)-(1+1))"))  # Expected: 0
    # print(calculate("(1+2)*3"))  # Expected: 9
    # print()

    # # Test: Exponentiation Associativity
    # print(calculate("2^2^3"))  # Expected: 256
    # print()

    # # Test: Rounding and Conversion to Int
    # print(calculate("1.23456"))  # Expected: 1.23456
    # print(calculate("1.00000"))  # Expected: 1
    # print()

    # # Test: Negative Numbers
    # print(calculate("-1+2"))  # Expected: 1
    # print()

    # # Test: Error Cases
    # try:
    #     print(calculate("1/0"))  # Expected: Error (division by zero) V
    # except Exception as e:
    #     print(e)

    # try:
    #     print(calculate("1+2*"))  # Expected: Error (syntax error) V
    # except Exception as e:
    #     print(e)

    # try:
    #     print(calculate("1++2"))  # Expected: Error (syntax error) V
    # except Exception as e:
    #     print(e)

    # try:
    #     print(calculate("(1+(2*3)"))  # Expected: Error (syntax error) V
    # except Exception as e:
    #     print(e)

    # try:
    #     print(calculate("1+(2*3))"))  # Expected: Error (syntax error) V
    # except Exception as e:
    #     print(e)

    # try:
    #     print(calculate("1.1.1+2"))  # Expected: Error (syntax error)
    # except Exception as e:
    #     print(e)

    # try:
    #     print(calculate("1#2"))  # Expected: Error (unsupported operation) V
    # except Exception as e:
    #     print(e)

    # # Test: Complex Operations
    # print()
    # print("Round 2")
    # print(calculate("((2+3)*4)^2"))  # Expected: 400
    # print(calculate("2^3^2"))  # Expected: 512
    # print(calculate("1+2*(3+4*5)^2"))  # Expected: 1059
    # print(calculate("((1+2)*(3+4))^2"))  # Expected: 441
    # print(calculate("2^2^2^2"))  # Expected: 65536
    # print(calculate("1.23456*2"))  # Expected: 2.46912
    # print(calculate("-1+2*3^4/5"))  # Expected: 31.4
    # print(calculate("1+(2-3*(4/5))^6"))  # Expected: 1.0041
    # print(calculate("1+2*3-4/5^6"))  # Expected: 6.999744
    # print()
