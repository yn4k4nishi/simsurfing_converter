#! /usr/bin/python3

import numpy as np
from scipy import optimize as opt
import matplotlib.pyplot as plt
import csv
import sys


def ref_func(x, a0, a1, a2, b0, b1, b2, b3, b4, b5, b6):
    return np.exp(a0 + a1*x + a2*x**2) * (b0 + b1*x + b2*x**2 + b3*x**3 + b4*x**4 + b5*x**5 + b6*x**6 )

def read_csv(file_name):
    x_data = np.array([])
    y_data = np.array([])

    with open(file_name, newline='') as file:
        reader = csv.reader(file, delimiter=',')

        header = reader.__next__()
        while header[0][0] == "#":
            header = reader.__next__()
        
        for row in reader:
            x_data = np.append(float(row[0])/1e9 , x_data)
            y_data = np.append(float(row[1])*1e12, y_data)
    
    return x_data, y_data

def get_func():
    args = sys.argv
    file = open(args[0], 'r').readlines()
    line_before = ""
    for line in file:
        if("def ref_func(" in line_before):
            print("target function")
            print('='*120)
            print(line_before, end='')
            print(line, end='')
            print('='*120)
            print()
            break

        line_before = line


if __name__ == "__main__":

    args = sys.argv

    if(len(args) < 2):
        print('Error: invaild argument.', file=sys.stderr)
        sys.exit(1)
    

    x_data, y_data = read_csv(args[1])

    popt, pcov = opt.curve_fit(ref_func, x_data, y_data)

    get_func()
    print("param index\t| value")
    print('-'*40)
    for i in range(len(popt)):
        print(i, "\t\t| ", popt[i])

    for a in args:
        if(a == "-p"):
            plt.xlabel("Freq[GHz]")
            plt.ylabel("[pF]")
            plt.scatter(x_data, y_data, color="r")
            plt.plot(x_data, ref_func(x_data, *popt))
            plt.show()
            break


