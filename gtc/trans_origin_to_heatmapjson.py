# -*- coding:utf8 -*-

import os
import csv
import json
import sys
import types
import time
#import gc
import random

#weight is the data of JF
#coordinate is the data of value

global total_string

#seperate the pairs(coordinate, weight) by hour
list_hour_origin = [[] for i in range(24)] 
list_hour_unique = [[] for i in range(24)] 

def decoder(filename, stamp_hour):
    with open(filename, "r") as F_in:
        dictionary = json.load(F_in)

    for i in range(len(dictionary["RWS"])):
        s1 = dictionary["RWS"][i]
        for j in range(len(s1["RW"])):
            s2 = s1["RW"][j]
            for k in range(len(s2["FIS"])):
                s3 = s2["FIS"][k]
                for l in range(len(s3["FI"])): 
                    s4 = s3["FI"][l] #each flow item

                    #get weight
                    weight = 0.0
                    for h in range(len(s4["CF"])):
                        s5 = s4["CF"][h] #current flow
                        weight = weight + float(s5.get("JF"))
                    weight = weight / len(s4["CF"])
                    
                    #get coordinates
                    flag = 0
                    for h in range(len(s4["SHP"])):
                        s5 = s4["SHP"][h]["value"]
                        for item in s5:
                            for co in item.split(' '):
                                x = 0.0
                                y = 0.0
                                cnt = 0
                                for t in co.split(','):
                                    if t == "":
                                        continue
                                    
                                    if cnt == 0:
                                        x = t
                                    else:
                                        y = t
                                    cnt = cnt + 1
                                if cnt == 2:
                                    if random.random() < 0.1:
                                        list_hour_origin[stamp_hour].append((x, y, weight))
                                    # flag = 1
                                    break
                                del x, y, cnt
                            # if flag == 1:
                            #     break
                        del s5
                        # if flag == 1:
                        #     break
                    del weight, s4 
                del s3
            del s2
        del s1

    '''list_coordinates_unique = []
    list_coordinates_unique = list(set(list_coordinates_origin))

    output_string = '{"features": ['
    for line in list_coordinates_unique:
        cnt = 0
        x = 0
        y = 0
        weight = 0
        for item in line:
            if cnt == 0:
                x = item
            if cnt == 1:
                y = item
            if cnt == 2:
                weight = item
            cnt = cnt + 1
        mystr = '{"coordinates": [%s, %s], "weight": %s}, ' %(x, y, weight)
        output_string = output_string + mystr

    output_string = output_string[:-2] + '], "hour": %d}' %(stamp_hour)

    global total_string
    total_string = total_string + output_string + ', '
    '''

if __name__ == '__main__':
    F_out = open("HeatmapInput_10percent_1101.js", "w")
    F_out.write('eqfeed_callback = ' + '\n')

    
    global total_string
    F_out.write('\'[{"contents": [')
    total_string = ""

    path = "speed_1101_true"
    files= os.listdir(path)
    for item in files:
        timeStamp = float(item[:-5])
        timeArray = time.localtime(timeStamp)
        file_hour = int(time.strftime("%H", timeArray))
        filename = path + '/' + item
        decoder(filename, file_hour)
    
    for stamp_hour in range(24):

        list_hour_unique[stamp_hour] = list(set(list_hour_origin[stamp_hour]))
        F_out.write('{"features": [')
        output_string = ''
        flag = 0
        for line in list_hour_unique[stamp_hour]:
            if flag == 1:
                F_out.write(', ')
            cnt = 0
            x = 0
            y = 0
            weight = 0
            for item in line:
                if cnt == 0:
                    x = item
                if cnt == 1:
                    y = item
                if cnt == 2:
                    weight = item
                cnt = cnt + 1
            #output_string = output_string + '{"coordinates": [%s, %s], "weight": %s}, ' %(x, y, weight)
            F_out.write('{"coordinates": [%s, %s], "weight": %s}' %(x, y, weight))
            flag = 1
            del x, y, cnt, weight
        '''
        if flag:
            output_string = output_string[:-2]
        output_string = output_string + '], "hour": %d}' %(stamp_hour)
        
        total_string = total_string + output_string + ', '

        del output_string
        '''
        F_out.write('], "hour": %d}' %(stamp_hour))
        if stamp_hour != 23:
            F_out.write(', ')
        else:
            F_out.write(']}]\';')

    '''
    total_string = total_string[:-2] + ']}]\';'
    print >> F_out, total_string
    '''

    F_out.close()
