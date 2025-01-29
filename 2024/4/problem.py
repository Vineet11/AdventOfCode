def parse_transposed_input(filename):
    with open(filename, 'r') as f:
        # Read all lines from the input file
        raw_data = f.read().strip().splitlines()
    return raw_data

# Usage example:
wordMatrix = parse_transposed_input('input.txt')
# wordMatrix = parse_transposed_input('sample.txt')

width = len(wordMatrix[0])
height = len(wordMatrix)

wordCount = 0
for i in range(height):
    for j in range(width):
        if wordMatrix[i][j] == "X":
            # For every X, we need to search in vertical(2), horizontal (2), diagonal (4)
            if i >= 3: 
                # search up:
                word = ''.join([wordMatrix[idx][j] for idx in range(i, i-4, -1)])
                if word == "XMAS":
                    wordCount += 1
            if i <= height - 4: 
                # search down:
                word = ''.join([wordMatrix[idx][j] for idx in range(i, i+4)])
                if word == "XMAS":
                    wordCount += 1
            if j >= 3: 
                # search left:
                word = ''.join([wordMatrix[i][idx] for idx in range(j, j-4, -1)])
                if word == "XMAS":
                    wordCount += 1
            if j <= width - 4: 
                # search right:
                word = ''.join([wordMatrix[i][idx] for idx in range(j, j+4)])
                if word == "XMAS":
                    wordCount += 1
            if i >=3 and j >=3:
                # search top left
                word = ''.join([wordMatrix[i + idx][j + idx] for idx in range(0, -4, -1)])
                if word == "XMAS":
                    wordCount += 1
            if i <= height - 4 and j <= width - 4:
                # search bottom right
                word = ''.join([wordMatrix[i + idx][j + idx] for idx in range(0, 4)])
                if word == "XMAS":
                    wordCount += 1
            if i >=3 and j <= width - 4:
                # search top right
                word = ''.join([wordMatrix[i - idx][j + idx] for idx in range(0, 4)])
                if word == "XMAS":
                    wordCount += 1
            if i <= height - 4 and j >=3:
                # search bottom left
                word = ''.join([wordMatrix[i + idx][j - idx] for idx in range(0, 4)])
                if word == "XMAS":
                    wordCount += 1

print(f"Word count is {wordCount}")

# Part 2:

wordCount = 0
for i in range(height):
    for j in range(width):
        if wordMatrix[i][j] == "A":
            # For every A, we need to search X pattern
            if (i >= 1 and i <= height - 2) and (j >= 1 and j <= width - 2):
                lTopRBtm = ''.join([wordMatrix[i + idx][j + idx] for idx in range(-1, 2)])
                lBtmRTop = ''.join([wordMatrix[i + idx][j - idx] for idx in range(-1, 2)])
                if (lTopRBtm =="MAS" or lTopRBtm == "SAM") and (lBtmRTop =="MAS" or lBtmRTop == "SAM"):
                    wordCount += 1

print(f"Updated word count is {wordCount}")