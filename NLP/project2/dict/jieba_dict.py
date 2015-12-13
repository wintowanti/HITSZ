
import jieba.posseg as pseg
import jieba

def get_surname(file_name):
    f = open(file_name)
    lines = f.readlines()
    surname = []
    for w in lines:
        surname.append(w.strip())
    return surname
    


def analyse(line, surname):
    words = []
    tags = []
    names = []
    jump = False
    vec = pseg.cut(line)
    for w,tag in vec:
        words.append(w)
        tags.append(tag)

        
    for i in range(len(tags)):
        if jump:
            jump = False
            continue
        if tags[i] == 'nr':
            if len(words[i]) > 1:
                names.append(words[i])
            else:
                ss = words[i].encode('utf-8')
                if ss in surname:
                    name = words[i] + words[i+1]
                    names.append(name)
                    jump = True
                else:
                    ss1 = words[i-1][-1:].encode('utf-8')
                    ss2 = words[i-1][-2:-1].encode('utf-8')
                    if ss1 in surname:
                        name = words[i-1][-2:] + words[i]
                        names.append(name)
                    elif ss2 in surname:
                        name = words[i-1][-2:] + words[i]
                        names.append(name)
        elif len(tags[i]) > 1:
            if tags[i][:2] == 'nr':
                ss = words[i][0].encode('utf-8')
                if ss in surname:
                    names.append(words[i])
    print line
    for i in range(len(tags)):
        print words[i],tags[i],' ',
    print '\n'
    print "Name:",
    for name in names:
        print name,
    print '\n'
                 
        
    

if __name__ == '__main__':
    jieba.load_userdict('./joey_name.txt')
    jieba.load_userdict('./bigname.txt')
    jieba.load_userdict('./famous_name.txt')
    jieba.load_userdict('./renmin.txt')
    file_name = 'F:surname_.txt'
    surname = get_surname(file_name)
    f = open('F:project2_TrainingSet7000')
    lines = f.readlines()
    for line in lines:
        vec = line.split('\t')
        analyse(vec[3], surname)



