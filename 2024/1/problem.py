def parse_transposed_input(filename):
    with open(filename, 'r') as f:
        # Read all lines from the input file
        raw_data = f.read().strip().splitlines()
    
    # Initialize the two lists
    list1 = []
    list2 = []
    
    for line in raw_data:
        # Split the line by spaces (or any other delimiter, e.g., comma)
        part1, part2 = line.split()
        
        # Append each part to the corresponding list
        list1.append(int(part1))
        list2.append(int(part2))
        
    return list1, list2

# Usage example:
list1, list2 = parse_transposed_input('input.txt')

list1.sort()
list2.sort()
# Part 1:
sum = 0
for a, b in zip(list1, list2):
    sum += abs(a - b)

print(f"Sum: {sum}")

# Part 2:
occurrenceDict = {}
for val in list2:
    if val in occurrenceDict:
        occurrenceDict[val] += 1
    else:
        occurrenceDict[val] = 1

similarityScore = 0
for val in list1:
    if val in occurrenceDict:
        similarityScore += val * occurrenceDict[val]

print(f"Similarity score: {similarityScore}")