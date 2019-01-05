# coding=utf-8

import codecs

# f1 = codecs.open(tf_train_dir + '/this_train_total_corpus.txt', 'w', encoding='utf8')
PROB_START = "data/prob_start.py"  # 初始状态概率
PROB_EMIT = "data/prob_emit.py"  # 计算给定标签下，观察值概率矩阵观察值是<St,Ot+1>而不是HMM的<St+1>求的是<St,Ot+1>条件下St+1的概率
# PROB_TRANS = "data/prob_trans.py"  # 不需要转移概率
start_fp = codecs.open(PROB_START, 'w', encoding='utf8')
emit_fp = codecs.open(PROB_EMIT, 'w', encoding='utf8')


# trans_fp = open(PROB_TRANS, 'w', encoding='utf8')不需要计算转移概率
def getList(input_str):  # 输入词语，输出状态
    """
    输入一个词语，然后把词语转化成B,M,E,S的形式
    :param input_str:
    :return:
    """
    outpout_str = []
    if len(input_str) == 1:
        outpout_str.append('S')
    elif len(input_str) == 2:
        outpout_str = ['B', 'E']
    else:
        M_num = len(input_str) - 2
        M_list = ['M'] * M_num
        outpout_str.append('B')
        outpout_str.extend(M_list)  # 把M_list中的'M'分别添加进去
        outpout_str.append('E')
    return outpout_str


def init():
    """
    初始化操作
    count_tag={}计算B,M,E,S每一个tag的数量
    trina_B={{},{},{},{}}通过字典嵌套计算转移概率
    emit_C计算<St,Ot+1>条件下St+1的概率S=[B,M,E,S]O表示word
    :return:
    """
    for A in tags:
        word_dict = {}
        for B in tags:
            gailv = {}
            for wordA in words_set:
                gailv[wordA] = 0
            word_dict[B] = gailv
        emit_C[A] = word_dict


tags = ["B", "M", "E", "S"]
o_tags = ["B", "M", "E", "S", "O", "start"]
initial = {}
file = codecs.open("trainCorpus.txt_utf8", "r", encoding="utf8")
words_set = set()
pre_a = {}  # 初始概率
line_number = 0  # 行数
all_words = []  # 词汇总
all_tags = []  # [B,M,E,S]标签汇总
# trina_B={}#不需要计算转移概率
emit_C = {}  # 发射概率
count_word = {}
count_tag = {}  # 计算[B,E,M,S]中每一个类别的字的总数
# 计算B，M，E，S的数量
for line in file:
    line = line.strip()
    # 生成词的set()
    word_list = []
    line_words = []
    line_number = line_number + 1
    for i in range(len(line)):
        if line[i] == " ":
            continue
        word_list.append(line[i])
        words_set.add(line[i])
    words = line.split(" ")
    print(word_list)
    all_words.append(word_list)
    line_tags = []
    for word in words:
        words_tags = getList(word)
        for tag in words_tags:
            line_tags.append(tag)
    print(line_tags)
    all_tags.append(line_tags)
for tag in tags:
    count_tag[tag] = 0
for A in tags:
    word_dict = {}
    for B in o_tags:
        gailv = {}
        for wordA in words_set:
            gailv[wordA] = 0
        word_dict[B] = gailv
    emit_C[A] = word_dict
# 计算初始概率
for line_tags in all_tags:
    lenght_tags = len(line_tags)
    if line_tags[0] in pre_a.keys():
        pre_a[line_tags[0]] = pre_a[line_tags[0]] + 1.0 / line_number
    else:
        pre_a[line_tags[0]] = 1.0 / line_number
    count_tag[line_tags[0]] = count_tag[line_tags[0]] + 1
start_fp.write(str(pre_a))
start_fp.close()
# 不需要计算转移概率
for line_tags in all_tags:
    lenght_tags = len(line_tags)
    for i in range(1, lenght_tags):
        count_tag[line_tags[i]] = count_tag[line_tags[i]] + 1
    # trina_B[line_tags[i-1]][line_tags[i]]=trina_B[line_tags[i-1]][line_tags[i]]+1
# 计算给定标签下，观察值概率矩阵观察值是<St,Ot+1>而不是HMM的<Ot+1>
for i in range(line_number):
    lenght = len(all_tags[i])
    for j in range(0, lenght):
        if j == 0:
            emit_C[all_tags[i][j]]["start"][all_words[i][j]] = emit_C[all_tags[i][j]]["start"][all_words[i][j]] + 1.0
        else:
            emit_C[all_tags[i][j]][all_tags[i][j - 1]][all_words[i][j]] = emit_C[all_tags[i][j]][all_tags[i][j - 1]][
                                                                              all_words[i][j]] + 1.0
# for linex,liney in zip(all_tags,all_words):
# 	for x,y in zip(linex,liney):
# 		emit_C[x][y]=emit_C[x][y]+1.0
for tag in tags:
    for key_pre in emit_C[tag].keys():
        for key_word in emit_C[tag][key_pre].keys():
            emit_C[tag][key_pre][key_word] = 1.0 * emit_C[tag][key_pre][key_word] / count_tag[tag]
emit_fp.write(str(emit_C))
emit_fp.close()
# for key in trina_B.keys():
# 	for other_key in trina_B[key].keys():
# 		trina_B[key][other_key]=1.0*trina_B[key][other_key]/count_tag[key]
for tag in count_tag.keys():
    print(tag, count_tag[tag])
# trans_fp.write(str(trina_B))
# trans_fp.close()
