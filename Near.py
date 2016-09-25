from data_extract import Question, Question_data

def Hamming_dis(word1,word2):
    dis = 0
    for i in word1:
        dis = dis+ (word2.count(i)>=1)
    return dis

def Near(question,question_data):
    type = question.type
    Dis = []
    for i in question_data.data:
        if question_data.data[i].type!=type:
            continue
        dis = Hamming_dis(question.word_info,question_data.data[i].word_info)
        Dis.append([question_data.data[i].id,dis])
    return Dis    
		
if __name__ == '__main__':

    question_info_path = 'Sorted_data/question_info_sort.txt'
    invited_info_path = 'Sorted_data/invited_info_train_question_sort.txt'

    question_data = Question_data(question_info_path,invited_info_path)
    
    s = Near(question_data.get_question("91ddbff126fca69a5fcd51135b7d272b"),question_data)

    ###print s

