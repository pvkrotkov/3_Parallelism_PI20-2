import multiprocessing as mp
import csv
def element(args):
    i, j = args[0]
    A = args[1]#запись аргуметов 1 элемента массива
    B = args[2]#запись аргуметов 2 элемента массива
    res = 0
    # get a middle dimension
    N = len(A[0]) or len(B)
    for k in range(N):
        res += int(A[i][k]) * int(B[k][j]) #высчитывание значений матрицы
    return res
def create_args(matrix1, matrix2):
    args = []
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            args.append(((i, j), matrix1, matrix2))
    return args
def result(matrix):
    f = open("result.csv", "w")
    for row in matrix:
        for col in row:
            f.write(str(col) + ";") #запись матрицы в файл
        f.write("\n")
def info(args):
    path = args[0]
    matrix = []
    with open(path, encoding="utf-8-sig") as csv_file:
        file_reader = csv.reader(csv_file, delimiter=";") #считывание информации из файлов
        for row in file_reader:
            matrix.append(row) #запись матрицы в массив
    return matrix
def main():
    A = "./A.csv"
    B = "./B.csv"
    pool = mp.Pool(processes=2) #количество используемых рабочих процессов
    matrix = []
    A, B = pool.map(info, [(A, ), (B, )]) #выполняет функцию info для каждого элемента последовательности
    args = create_args(A, B) #аргументы матриц
    pool = mp.Pool(processes=(len(A) * len(B[0])))
    result_matrix = pool.map(element, args) #высчитывание матрицы
    k = 0
    for i in range(len(A)):
        matrix.append([]) #массив для новой строки

        for _ in range(len(B[0])):
            matrix[i].append(result_matrix[k]) #вписывает в массив строку новой матрицы
            k += 1

    result(matrix) #запись результата в файл


if __name__ == "__main__":
    main()
