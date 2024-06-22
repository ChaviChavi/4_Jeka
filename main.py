

import copy


class Atomic:
    def __init__(self, data, deep=False):
        self.original = data
        self.copy = copy.deepcopy if deep else copy.copy

        if isinstance(data, list):
            self.original_update = self.original.extend
        elif isinstance(data, (set, dict)):
            self.original_update = self.original.update

    def __enter__(self):
        self.data = self.copy(self.original)
        return self.data

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.original.clear()
            self.original_update(self.data)
        return True





# 1
numbers = [1, 2, 3, 4, 5]

with Atomic(numbers) as atomic:
    atomic.append(6)
    atomic[2] = 0
    del atomic[1]
print(numbers, 1)
#assert numbers == [1, 0, 4, 5, 6], '1'

# 2
numbers = [1, 2, 3, 4, 5]

with Atomic(numbers) as atomic:
    atomic.append(6)
    atomic[2] = 0
    del atomic[100]  # обращение по несуществующему индексу
print(numbers, 2)
#assert numbers == [1, 2, 3, 4, 5], '2'

# 3
matrix = [[1, 2], [3, 4]]

with Atomic(matrix) as atomic:
    atomic[1].append(0)  # изменение вложенной структуры
    atomic.append([5, 6])
    del atomic[100]  # обращение по несуществующему индексу

print(matrix, 3)
#assert matrix == [[1, 2], [3, 4, 0]], '3'

#4
matrix = [[1, 2], [3, 4]]

with Atomic(matrix, True) as atomic:
    atomic[1].append(0)       # изменение вложенной структуры
    atomic.append([5, 6])
    del atomic[100]           # обращение по несуществующему индексу

print(matrix,4)

print()
numbers = {1, 2, 3, 4, 5}

#5
with Atomic(numbers) as atomic:
    atomic.add(6)
    atomic.append(7)           # добавление элемента с помощью несуществующего метода

print(sorted(numbers),6)

with Atomic(numbers) as atomic:
    atomic.add(6)

print(sorted(numbers),6)

#6
print()
data = {'firstname': 'Alyson', 'lastname': 'Hannigan', 'birthday': {'day': 24, 'month': 'March', 'year': 1974}}

with Atomic(data, True) as atomic:          # deep = True
    atomic['birthday']['month'] = 'April'   # изменение вложенной структуры
    print(atomic['name'])                   # обращение по несуществующему ключу

print(data)

with Atomic(data) as atomic:                # deep = False
    atomic['birthday']['month'] = 'April'   # изменение вложенной структуры
    print(atomic['name'])                   # обращение по несуществующему ключу

print(data)
