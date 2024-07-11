# Построй диаграмму рассеяния для двух наборов случайных данных,
# сгенерированных с помощью функции `numpy.random.rand`.
# import numpy as np
# random_array = np.random.rand(5) # массив из 5 случайных чисел
# print(random_array)

import numpy as np
import matplotlib.pyplot as plt

# Генерация массивов случайных чисел
x = np.random.rand(100)  # массив из 100 случайных чисел для оси x
y = np.random.rand(100)  # массив из 100 случайных чисел для оси y

# Построение диаграммы рассеяния
plt.scatter(x, y)
plt.title('Диаграмма рассеяния случайных данных')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

# Генерация и вывод массива из 5 случайных чисел
random_array = np.random.rand(5)
print(random_array)