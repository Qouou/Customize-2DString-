import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import pandas as pd
import csv
from collections import defaultdict
import matplotlib.colors
import sys
import time

def segment(data):
    data = float(data)
    if data == -1:
        return 'white'
    elif data < 7.5:
        return 'lightgreen'
    elif data > 7.4 and data < 15.5:
        return 'LightSeaGreen'
    elif data > 15.4 and data < 25.5:
        return 'lightyellow'
    elif data > 25.4 and data < 35.5:
        return 'yellow'
    elif data > 35.4 and data < 45.5:
        return 'orange'
    elif data > 45.4 and data < 54.5:
        return 'tomato'
    elif data > 54.4 and data < 102.5:
        return 'IndianRed'
    elif data > 102.4 and data < 150.5:
        return 'red'
    elif data > 150.4 and data < 250.5:
        return 'purple'
    else:
        return 'brown'

def drawColor(data):
    ax = plt.subplot(111)

    tmp = data
    for j in range(len(tmp)):
        x = np.linspace(10 * int((j%10)), 10 * int((j%10)) + 10, 10)
        ax.fill_between(x,90 - 10 * int((j/10)), 100 - 10 * int((j/10)), facecolor = segment(tmp[j]))

    plt.xlim(0, 100)
    plt.ylim(0, 100)
    
    ax.xaxis.set_major_locator(MultipleLocator(10)) # 數字間隔 10
    ax.yaxis.set_major_locator(MultipleLocator(10)) # 設定 y 數字間隔 10
    ax.xaxis.grid(False,which='major') # major,color='black'
    ax.yaxis.grid(False,which='major') # major,color='black'
    ax.xaxis.set_ticks([]) # 去掉外標線
    ax.yaxis.set_ticks([])
    plt.axis('off')
    now = time.strftime("%Y-%m-%d-%H-%M", time.localtime())
    # date = date.replace('/','-').replace(' ','-').replace(':','-')
    plt.savefig('../static/sis/'+now + '.png', bbox_inches='tight',pad_inches = 0)
    plt.cla()
    plt.clf()
    return now
    # plt.show()

def main(argv):
    # print(len(argv))
    global plt 
    inputData = argv
    print(drawColor(inputData))
    

if __name__ == '__main__':
    main(sys.argv[1:])
