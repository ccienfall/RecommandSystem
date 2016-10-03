#Finding near user or question using hamming distance.
from data_extract import *
from operator import itemgetter, attrgetter

<<<<<<< HEAD

'''
Finding near user or question using hamming distance.

'''

=======
'''
>>>>>>> 8b4ab6d05da5558e8509a66eae1057a6ca7c994d
def Hamming_dis(word1,word2):
    dis = 0
    for i in word1:
        dis = dis+ (word2.count(i)>=1)
    return dis
'''

def compute_similar(word1,word2):
    dis = 0
    for i in word1:
        dis = dis+ (word2.count(i)>=1)
    return dis/float(len(list(set(word1+word2))))

def Near_question(question,question_data):
    type = question.type
    Dis = []
    for i in question_data.data:
        #delete itself
        if question_data.data[i].type!=type or question_data.data[i].id == question.id:
            continue
        score = compute_similar(question.word_info,question_data.data[i].word_info)
        #if dis >= 1:
        Dis.append([question_data.data[i].id,score])
    Dis = sorted(Dis,key=itemgetter(1,0))[::-1] #reverse the list
    Dis = Dis[0:10]
    return Dis

def Near_user(user,user_data):
    Dis = []
    max_word_info_score = 0.001
    max_type_score = 0.001
    for i in user_data.data:
        #delete itself
        if user_data.data[i].id == user.id:
            continue
        word_info_score = compute_similar(user.word_info,user_data.data[i].word_info)
        type_score = compute_similar(user.type,user_data.data[i].type)
        if word_info_score > max_word_info_score: max_word_info_score = word_info_score
        if type_score > max_type_score: max_type_score = type_score
        #if type_dis >= 1 and word_info_dis >= 1:
        #score = word_info_score * 4.0 + type_score * 1.0
        Dis.append([user_data.data[i].id, word_info_score, type_score])
    for dis in Dis:#regulization the score and compute total score
        dis[1] = round(dis[1] / max_word_info_score, 3)
        dis[2] = round(dis[2] / max_type_score,3)
        score = ( dis[1] + dis[2] )
        dis.append(round(score,3))
    Dis = sorted(Dis,key=itemgetter(3,1,2,0))[::-1]
    return Dis

def get_candidate_user(user,candidate_num,user_data):
    candidate_user_list = Near_user(user,user_data)[0:candidate_num]
    return candidate_user_list

def get_candidate_question(question,candidate_user_list,user_data,question_data):
    candidate_question_list = []
    max_user_score = 0.001
    max_question_score = 0.001
    for user_line in candidate_user_list:
        user_id = user_line[0]
        user_score = user_line[3]
        for question_id in user_data.get_user(user_id).ans_question:
            question_score = round(compute_similar(question_data.get_question(question_id).word_info,question.word_info),3)
            candidate_question_list.append([question_id, user_score, question_score])
    for candidate_question in candidate_question_list:
        if candidate_question[1] > max_user_score : max_user_score = candidate_question[1]
        if candidate_question[2] > max_question_score : max_question_score = candidate_question[2]
    for candidate_question in candidate_question_list:
        user_score = candidate_question[1] / max_user_score
        question_score = candidate_question[2] / max_question_score
        score = (user_score + question_score)/2
        #del candidate_question[2],candidate_question[1]
        candidate_question.append(round(score,3))
    candidate_question_list = sorted(candidate_question_list,key=itemgetter(3,0))[::-1]
    return candidate_question_list

def print_list(list):
    for i in list:
        print i

if __name__ == '__main__':

    #initailize the data
    question_info_path = '../question_info_sort.txt'
    invited_info_path = '../invited_info_train_question_sort.txt'
    user_info_path = "../user_info_sort.txt"
    question_data = Question_data(question_info_path,invited_info_path)
    user_data = User_data(user_info_path,invited_info_path)

    output_path = "../output.txt"
    output_file = open(output_path,'w')

    #show the closest question and user for each (qid,uid) in validata_nolabel.txt
    validate_file = file("../validate_nolabel.txt")
    line = validate_file.readline()
    line = validate_file.readline().strip("\r\n")
    while line :
        question_id = line.split(',')[0]
        user_id = line.split(',')[1]
        '''
        closest_question = Near_question(question_data.get_question(question_id),question_data)[0:10]
        closest_user = Near_user(user_data.get_user(user_id),user_data)[0:3]
        '''
        candidate_user_list = get_candidate_user(user_data.get_user(user_id),50,user_data)
        candidate_question_list = get_candidate_question(question_data.get_question(question_id),candidate_user_list,user_data,question_data)


        score = 0.0
        for candidate_question in candidate_question_list:
            if question_id == candidate_question[0]:
                score = candidate_question[3]
        result = question_id + "," + user_id + "," + str(score)
        print result

        output_file.write(result)
        output_file.write("\n")

        #print "**********" + user_id + "********** similar users: *****************************************************"
        #print_list(candidate_user_list)
        #print "**********question score ***********"
        #print_list(candidate_question_list)
        line = validate_file.readline().strip("\r\n")
