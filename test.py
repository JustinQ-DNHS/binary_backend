array = []

path = "samplepathname"

print(path[1])

for i in range(len(path)):
    array.append(hex(ord(path[i]))[2:])

print(''.join(array))
output = []

for i in range(len(array)):
    output.append(chr(int(array[i], 16)))

print(''.join(output))
    