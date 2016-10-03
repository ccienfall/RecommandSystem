#!/usr/bin/env python
# coding=utf-8

from recsys.algorithm.factorize import SVD
svd = SVD()
svd.load_data(filename='../invited_info_train_question_sort.txt', sep='\t', format={'col':0, 'row':1, 'value':2, 'ids':str})
k = 100
svd.compute(k=k,savefile='/home/xiatian/RecommandSystem/tmp/weight')

svd2 = SVD(filename='/home/xiatian/RecommandSystem/tmp/weight') # Loading already computed SVD model

output_path = "./output.txt"
output_file = open(output_path,'w')
validate_file = file("../validate_nolabel.txt")
line = validate_file.readline()
line = validate_file.readline().strip("\r\n")

while line :
    question_id = line.split(',')[0]
    user_id = line.split(',')[1]
    try:
        predict = svd2.predict(user_id,question_id,0.0,1.0)
    except:
        predict = 0
        print question_id + "," + user_id + "      Exception"

    if predict > 1.0: predict = 1.0
    if predict < 0.0001:predict = 0.0
    result = question_id + "," + user_id + "," + str(predict)
    #print result

    output_file.write(result)
    output_file.write("\n")
    line = validate_file.readline().strip("\r\n")


