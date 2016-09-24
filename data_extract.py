class Question:
    id = None
    user = []
    type = None
    word_info = []
    letter_info = []
    good_ans_num = 0
    average_click_like = 0
    def __init__(self,id,type,word_info,letter_info,good_ans_num,average_click_like):
        self.id = id
        self.type = type
        self.word_info = word_info
        self.letter_info = letter_info
        self.good_ans_num = good_ans_num
        self.average_click_like = average_click_like
        self.ans_user = []
        self.unans_user = []
    def add_user(self,user,ans):
        if ans == "1":
            self.ans_user.append(user)
        elif ans == "0":
            self.unans_user.append(user)

class Question_data:
    def __init__(self,qusetion_info_path,invited_info_path):
        question_file = file(qusetion_info_path)
        line = question_file.readline()
        self.data = dict()
        while line:
            info = line.split()
            avarage_click_like = 0
            if float(info[5]) == 0:
                avarage_click_like = 0
            else:
                avarage_click_like = float(info[4])/float(info[5])
            question = Question(info[0],
                                info[1],
                                info[2].split("/"),
                                info[3].split("/"),
                                int(info[6]),
                                avarage_click_like)
            #print question
            self.data[question.id] = question
            line = question_file.readline()
        invited_file= file(invited_info_path)
        line = invited_file.readline()

        while line:
            info = line.split()
            self.data[info[0]].add_user(info[1],info[2])
            line = invited_file.readline()

    def get_question(self,id):
        return self.data[id]


if __name__ == "__main__":
    question_info_path = "Sorted_data/question_info_sort.txt"
    invited_info_path = "Sorted_data/invited_info_train_question_sort.txt"
    question_data = Question_data(question_info_path,invited_info_path)
    print question_data.get_question("91ddbff126fca69a5fcd51135b7d272b").unans_user

