import multiprocessing as mp
import csv
from random import randint

def reading_from_file(args):
    """
    Функция чтение матриц из файла.
    """
    path = args[0]
    matrix = []
    with open(path, encoding="utf-8-sig") as csv_file:
        file_reader = csv.reader(csv_file, delimiter=";")
        for row in file_reader:
            matrix.append(row)
    return matrix

def write_to_file(matrix):
    f = open("result_matrix.csv", "w")
    for row in matrix:
        for col in row:
            f.write(str(col) + ";")
        f.write("\n")

def element(args):
    i, j = args[0]
    matrix1 = args[1]
    matrix2 = args[2]
    res = 0
    # get a middle dimension
    N = len(matrix1[0]) or len(matrix2)
    for k in range(N):
        res += int(matrix1[i][k]) * int(matrix2[k][j])
    with open('temp_results.csv', 'a+') as temp_file: # файл с промежуточными результами
        writer = csv.writer(temp_file, delimiter=';')
        writer.writerow([res])
    return res

def gen_args(matrix1, matrix2):
    args = []
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            args.append(((i, j), matrix1, matrix2))
    return args

def gen_matrix(n, filename):
    matrix = [[randint(0,10) for i in range(n)] for j in range(n)]

    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';', lineterminator="\n")
        for row in matrix:
            writer.writerow(row)

    print(matrix)

def main():
    rows = ''
    while True:

        path1 = "./matrix1.csv" #путь до первой матрицы
        path2 = "./matrix2.csv" #путь до второй матрицы

        rows = int(input('Введите 0, чтобы завершить программу, или размерность матрицы для ее генерации: '))
        if not rows:
            break

        gen_matrix(rows, path1)
        gen_matrix(rows, path2)

        pool = mp.Pool(processes=2)
        matrix = []
        matrix1, matrix2 = pool.map(reading_from_file, [(path1, ), (path2, )])
        args = gen_args(matrix1, matrix2)
        pool = mp.Pool(processes=(len(matrix1) * len(matrix2[0])))
        result_matrix = pool.map(element, args)
        k = 0
        for i in range(len(matrix1)):
            matrix.append([])
            for _ in range(len(matrix2[0])):
                matrix[i].append(result_matrix[k])
                k += 1
        write_to_file(matrix)

if __name__ == "__main__":
    main()
