def parse_input(filename):
    # Split input into two parts based on the empty line separator
    with open(filename, 'r') as f:
        parts = f.read().strip().split('\n\n')

    # Function to convert the first part (split by '|') into a list of lists
    def convert_first_part(part):
        return [line.split('|') for line in part.splitlines()]

    # Function to convert the second part (split by ',') into a list of lists
    def convert_second_part(part):
        return [line.split(',') for line in part.splitlines()]

    # Convert both parts into list of lists
    rules = convert_first_part(parts[0])
    pagePrinting = convert_second_part(parts[1])

    return rules, pagePrinting

# Usage example:
# rules, pagePrinting = parse_input('sample.txt')
rules, pagePrinting = parse_input('input.txt')
# Part 1
# convert rules to dictionary
ruleDict = {}
for rule in rules:
    before, after = rule[0], rule[1]
    if not after in ruleDict:
        ruleDict[after] = {}
    ruleDict[after][before] = 0

correctCount = 0
correctCountSum = 0
for pages in pagePrinting:
    correctOrder = True
    seqLen = len(pages)
    for i in range(seqLen):
        page = pages[i]
        if page in ruleDict:
            pageBeforeRule = ruleDict[page]
            pagesAfter = pages[i+1::]
            for pageAfter in pagesAfter:
                if pageAfter in pageBeforeRule:
                    correctOrder = False
    if correctOrder:
        correctCount += 1
        correctCountSum += int(pages[seqLen//2])

print(f"Correct count is {correctCount}")
print(f"Correct sum is {correctCountSum}")