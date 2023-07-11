def create_permutation (array:list, length:int, required_length:int, alowed_values:list):
    if length == required_length:
        number = alowed_values[0]
        array.append(number)
        main_array.append(array.copy())
        array.pop(len(array) - 1)
    else:
        length += 1
        for number in alowed_values.copy():
            array.append(number)
            alowed_values.remove(number)
            create_permutation(array, length, required_length, alowed_values)
            array.pop(len(array) - 1)
            alowed_values.append(number)



def start_permutation (required_length:int):
    array = []
    length = 1
    alowed_values = []
    for number in range(1, required_length + 1):
        alowed_values.append(number)
    create_permutation(array, length, required_length, alowed_values)


required_length = 6

main_array = []
start_permutation(required_length)

for array in main_array.copy():
    print(array)



print(len(main_array))