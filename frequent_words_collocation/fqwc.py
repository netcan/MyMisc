from collections import defaultdict
import operator


class Word:
    def __init__(self):
        self.prev_words = defaultdict(int)
        self.next_words = defaultdict(int)
        self.prev_words_x = None
        self.next_words_x = None
        self.cnt = 1

    def add_prev(self, word):
        self.prev_words[word] += 1

    def add_next(self, word):
        self.next_words[word] += 1

    def sort_collocation(self):
        self.prev_words_x = sorted(self.prev_words.items(), key=lambda x: x[1], reverse=True)
        self.next_words_x = sorted(self.next_words.items(), key=lambda x: x[1], reverse=True)
        return self

    def __iadd__(self, other):
        self.cnt += other
        return self

    def __repr__(self):
        return str(self.cnt)

    def __lt__(self, other):
        return self.cnt < other.cnt


def get_fqwc(file='wiki_zh_test'):
    word_fq = {}
    with open(file + '.txt', 'r') as f:
        for line in f:
            words = line.split(' ')
            for idx, word in enumerate(words):
                word = word.strip()
                if word in word_fq:
                    word_fq[word] += 1
                else:
                    word_fq[word] = Word()

                if idx > 0:
                    word_fq[word].add_prev(words[idx - 1])
                if idx + 1 < len(words):
                    word_fq[word].add_next(words[idx + 1])

    word_fq = {k: v.sort_collocation() for k, v in word_fq.items()}
    word_fq = sorted(word_fq.items(), key=lambda x: x[1], reverse=True)
    # print(word_fq)

    with open(file + '_out.txt', 'w') as f:
        for word in word_fq:
            f.write('{}({})\n'.format(word[0], word[1]))
            try:
                f.write('Prev Words: ')
                for pw in word[1].prev_words_x:
                    f.write('{}({}) '.format(pw[0], pw[1]))
            except TypeError:
                pass
            f.write('\n')

            try:
                f.write('Next Words: ')
                for nw in word[1].next_words_x:
                    f.write('{}({}) '.format(nw[0], nw[1]))
            except TypeError:
                pass
            f.write('\n')



if __name__ == '__main__':
    get_fqwc()