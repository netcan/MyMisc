
def delete_nest_label(sentences, open_label='<BEGIN_E>', close_label='<END_E>'):
    # 将开、闭标签用数字来代替
    sts = sentences.replace(open_label, chr(2)).replace(close_label, chr(3))
    brace = []
    ret = ""
    for letter in sts:
        insert_letter = True
        if letter == chr(2):
            if len(brace): insert_letter = False     # 嵌套的情况
            brace.append(letter)
        elif letter == chr(3):
            try:
                brace.pop()
                if len(brace): insert_letter = False # 嵌套的情况
            except IndexError:
                return sentences                     # 只有)的情况

        if insert_letter:
            ret += letter
    ret = ret.replace(chr(2), open_label).replace(chr(3), close_label)
    return ret


def handle_file(file):
    with open(file + '.txt', 'r') as f:
        with open(file + '_handled.txt', 'w') as ff:
            ff.writelines([delete_nest_label(sentences) for sentences in f])



