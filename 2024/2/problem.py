def parse_transposed_input(filename):
    with open(filename, 'r') as f:
        # Read all lines from the input file
        raw_data = f.read().strip().splitlines()
    
    lists = [list(map(int, line.split())) for line in raw_data]
        
    return lists

# Usage example:
reports = parse_transposed_input('input.txt')
# reports = parse_transposed_input('sample.txt')

# Part 1
validReportCnt = 0
for report in reports:
    isValid = True
    isAscending = (report[1] - report[0]) > 0
    multiplier = 1 if isAscending else -1
    for i in range(len(report) - 1):
        diff = multiplier*(report[i+1] - report[i])
        if diff > 3 or diff < 1:
            isValid = False
            break
    if isValid:
        validReportCnt += 1

print(f"Valid report count: {validReportCnt}")

# Part 2
validReportCnt = 0
for report in reports:
    isValid = True
    multiplier = 1
    safetySwitch = True
    # majority voting
    if len(report) < 4:
        # this case need to be handled differently
        raise
    for j in range(3):
        isAscending = (report[j + 1] - report[j]) > 0
        multiplier += 1 if isAscending else -1
    multiplier = 1 if multiplier > 0 else -1
    skipIndex = -1
    for i in range(len(report) - 1):
        if i == skipIndex:
            continue
        diff = multiplier*(report[i+1] - report[i])
        if diff > 3 or diff < 1:
            if not safetySwitch:
                isValid = False
                break
            else:
                if i == len(report) - 2:
                    safetySwitch = False
                    skipIndex = i + 1
                    continue
                else:                        
                    # try replacing i+1 th location
                    diff = multiplier*(report[i+2] - report[i])
                    if diff <= 3 and diff >= 1:
                        safetySwitch = False
                        skipIndex = i + 1
                        continue
                    else:
                        if i == 0:
                            safetySwitch = False
                            skipIndex = i
                            continue
                        # try replacing i = 0 index
                        diff = multiplier*(report[i+1] - report[i-1])
                        if diff <= 3 and diff >= 1:
                            safetySwitch = False
                            skipIndex = i
                            continue
                        else:
                            isValid = False
                            break
    if isValid:
        validReportCnt += 1

print(f"Updated valid report count: {validReportCnt}")
