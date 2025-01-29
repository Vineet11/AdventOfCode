def parse_transposed_input(filename):
    with open(filename, 'r') as f:
        # Read all lines from the input file
        raw_data = f.read().strip().splitlines()
    return raw_data

# Usage example:
corruptedMemory = parse_transposed_input('input.txt')
# corruptedMemory = parse_transposed_input('sample.txt')
# Part 1: xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
# Part 2: xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))

# create a state-machine
waitForMul = True
operatorString = ""
waitForNum1 = False
num1_str = ""
num1 = 1
waitForNum2 = False
num2_str = ""
num2 = 1
digitCount = 0

def resetStates():
    global waitForMul, operatorString, waitForNum1, num1_str, num1, waitForNum2, num2_str, num2, digitCount, resetMachine
    waitForMul = True
    operatorString = ""
    waitForNum1 = False
    num1_str = ""
    num1 = 1
    waitForNum2 = False
    num2_str = ""
    num2 = 1
    return

accumulatedSum = 0
for line in corruptedMemory:
    for char in line:
        if waitForMul:
            if operatorString == "":
                if char == "m":
                    operatorString += char
            elif operatorString == "m":
                if char == "u":
                    operatorString += char
                else:
                    resetStates()
            elif operatorString == "mu":
                if char == "l":
                    operatorString += char
                else:
                    resetStates()
            elif operatorString == "mul":
                if char == "(":
                    operatorString = ""
                    waitForNum1 = True
                    waitForMul = False
                else:
                    resetStates()
        elif waitForNum1:
            if char == ",":
                if len(num1_str) == 0 or len(num1_str) >3:
                    resetStates()
                else:
                    num1 = int(num1_str)
                    waitForNum2 = True
                    waitForNum1 = False
            elif char.isdigit():
                num1_str += char
            else:
                resetStates()
        elif waitForNum2:
            if char == ")":
                if len(num2_str) == 0 or len(num2_str) >3:
                    resetStates()
                else:
                    num2 = int(num2_str)
                    accumulatedSum += num2 * num1
                    resetStates()
            elif char.isdigit():
                num2_str += char
            else:
                resetStates()

print(f"Accumulated sum is {accumulatedSum}")

# Part 2

gateFactor = 1
resetStates()
accumulatedSum = 0
for line in corruptedMemory:
    for char in line:
        if waitForMul:
            if operatorString == "":
                if char == "m":
                    operatorString += char
            elif operatorString == "m":
                if char == "u":
                    operatorString += char
                else:
                    resetStates()
            elif operatorString == "mu":
                if char == "l":
                    operatorString += char
                else:
                    resetStates()
            elif operatorString == "mul":
                if char == "(":
                    operatorString = ""
                    waitForNum1 = True
                    waitForMul = False
                else:
                    resetStates()
        elif waitForNum1:
            if char == ",":
                if len(num1_str) == 0 or len(num1_str) >3:
                    resetStates()
                else:
                    num1 = int(num1_str)
                    waitForNum2 = True
                    waitForNum1 = False
            elif char.isdigit():
                num1_str += char
            else:
                resetStates()
        elif waitForNum2:
            if char == ")":
                if len(num2_str) == 0 or len(num2_str) >3:
                    resetStates()
                else:
                    num2 = int(num2_str)
                    accumulatedSum += gateFactor * num2 * num1
                    resetStates()
            elif char.isdigit():
                num2_str += char
            else:
                resetStates()
        if waitForMul:
            if operatorString == "":
                if char == "d":
                    operatorString += char
            elif operatorString == "d":
                if char == "o":
                    operatorString += char
                else:
                    resetStates()
            elif operatorString == "do":
                if char == "n":
                    operatorString += char
                else:
                    # just do detected
                    gateFactor = 1
                    resetStates()
            elif operatorString == "don":
                if char == "'":
                    operatorString += char
                else:
                    resetStates()
            elif operatorString == "don'":
                if char == "t":
                    operatorString += char
                    gateFactor = 0
                    resetStates()
                else:
                    resetStates()

print(f"New accumulated sum is {accumulatedSum}")