from data_extract import *
from operator import itemgetter, attrgetter

def Hamming_dis(word1,word2):
    dis = 0
    for i in word1:
        dis = dis+ (word2.count(i)>=1)
    return dis

def Near_question(question,question_data):
    type = question.type
    Dis = []
    for i in question_data.data:
        #delete itself
        if question_data.data[i].type!=type or question_data.data[i].id == question.id:
            continue
        dis = Hamming_dis(question.word_info,question_data.data[i].word_info)
        #if dis >= 1:
        Dis.append([question_data.data[i].id,dis])
    Dis = sorted(Dis,key=itemgetter(1,0))[::-1]#reverse the list
    return Dis

def Near_user(user,user_data):
    Dis = []
    for i in user_data.data:
        #delete itself
        if user_data.data[i].id == user.id:
            continue
        word_info_dis = Hamming_dis(user.word_info,user_data.data[i].word_info)
        type_dis = Hamming_dis(user.type,user_data.data[i].type)
        #if type_dis >= 1 and word_info_dis >= 1:
        Dis.append([user_data.data[i].id,word_info_dis,type_dis])
    Dis = sorted(Dis,key=itemgetter(2,1,0))[::-1]
    return Dis

if __name__ == '__main__':

    question_info_path = '../question_info_sort.txt'
    invited_info_path = '../invited_info_train_question_sort.txt'
    user_info_path = "../user_info_sort.txt"
    question_data = Question_data(question_info_path,invited_info_path)
    user_data = User_data(user_info_path,invited_info_path)

    #show the closest question and user for each (qid,uid) in validata_nolabel.txt
    validate_file = file("../validate_nolabel.txt")
    line = validate_file.readline()
    line = validate_file.readline().strip("\r\n")
    while line :
        question_id = line.split(',')[0]
        closest_question = Near_question(question_data.get_question(question_id),question_data)[0]
        user_id = line.split(',')[1]
        closest_user = Near_user(user_data.get_user(user_id),user_data)[0]
        print closest_question
        line = validate_file.readline().strip("\r\n")
