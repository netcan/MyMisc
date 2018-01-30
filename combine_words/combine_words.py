from collections import defaultdict


def find(union, x):
    if x == union[x]:
        return x
    else:
        union[x] = find(union, union[x])
        return union[x]


def unite(union, x, y):
    x = find(union, x)
    y = find(union, y)
    union[y] = x


def combine_words(file):
    words = open(file).readlines()
    line_of_word = defaultdict(list)
    # 删除尾部的换行
    words = [line.strip() for line in words]

    union = list(range(len(words)))

    for line_num, line in enumerate(words):
        for word in line.split(' '):
            line_of_word[word].append(line_num)

    for line_num, line in enumerate(words):
        for word in line.split(' '):
            for pointTo in line_of_word[word]:
                if pointTo != line_num:
                    unite(union, line_num, pointTo)

    result = defaultdict(set)
    for line_num, line in enumerate(words):
        result[find(union, line_num)].update(line.split(' '))

    ret = [' '.join(item) + '\n' for item in result.values()]
    return ret


if __name__ == '__main__':
    print(combine_words('words.txt'))
    with open('words_combined.txt', 'w') as f:
        f.writelines(combine_words('words.txt'))
