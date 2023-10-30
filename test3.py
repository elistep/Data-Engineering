import math
filename = 'text_3_var_57'
with open(filename) as file:
    lines = file.readlines()

matrix = list()

for line in lines:
    #print(line.strip())
    nums = line.strip().split(",")
    for i in range(len(nums)):
        if nums[i] == 'NA':
            nums[i] = str((int(nums[i-1])+int(nums[i+1]))/2)

    filtered = list()
    for item in nums:
        num = float(item)
        if math.sqrt(num) > 107:
            filtered.append(num)

    matrix.append(filtered)

#print(matrix)

with open('r_text_3.txt','w') as result:
    for row in matrix:
        for num in row:
            result.write(str(num) + ',')
        result.write("\n")

