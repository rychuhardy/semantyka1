import csv

outfile = 'out.txt'
directory_name = './data/'
filenames = [
    'dziecko.csv',
    'chlopiec.csv',
    'dziewczyna.csv',
    'maly.csv'
]

edges_list = []

class NetworkXEdge:
    def __init__(self, left_word, right_word, weight):
        if type(left_word) is not str:
            raise ValueError("left_word is not string", left_word)
        if type(right_word) is not str:
            raise ValueError("right_word is not string", right_word)
        weight = int(weight)
        self.left = left_word
        self.right = right_word
        self.weight = weight

    def to_string(self):
        return self.left + ';' + self.right + ';' + str(self.weight)

#From https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance
def lev(s, t):
    if s == t: return 0
    if abs(len(s)-len(t)) > 1: return 10
    elif len(s) == 0: return len(t)
    elif len(t) == 0: return len(s)
    v0 = [None] * (len(t) + 1)
    v1 = [None] * (len(t) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]

    return v1[len(t)]


#Polish words from sjp.pl
words = []
with open("slowa.txt", encoding='UTF-8') as f:
    words = f.readlines()
words = [x.strip() for x in words]

# counter of each word occurence
words_count = dict()
# Words that were replaced because they are not in the dictionary
replacements = dict()
# Empty answer or string PUSTE
special_answers = []

expressions = []

rejected = []

#Looks for similar word
def get_similar_words(word):
    for w in words:
        levs = lev(word, w)
        if levs < 2:
            if w in words_count:
                yield (w, words_count[w], levs)
            else:
                yield (w, 0, levs)

def replace_single_word(word, counter):

    if(word.strip().lower() == 'puste' or word.strip() == ''):
        special_answers.append(word)
        return None

    similar = list(get_similar_words(word))
    if counter > 2: # Document this
        return word
    elif len(similar) == 0:
        rejected.append(word)
        return None
    else:
        # sort by lev distance then by occurences count
        similar.sort(key=lambda sim: (sim[1], sim[2]))
        return similar[0][0]


def replace_expression(expr, counter):
    expressions.append(expr)
    return expr





def add_to_words_count(word, counter, key):

    if key or word in words:
        if word in words_count:
            words_count[word] += counter
        else:
            words_count[word] = counter
        return word

    if len(word.split()) > 1:
        return replace_expression(word, counter)

    else:
        replaced = replace_single_word(word, counter)
        if replaced is None:
            return None
        if replaced != word:
            replacements[word] = replaced
        return replaced


with open(outfile, 'a', encoding='utf-8') as output:
    for filename in filenames:
        with open(directory_name + filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            parsed_list = list(reader)
            for item in parsed_list:
                edge_name = filename.replace('.csv', '')
                word = item[1]
                counter = int(item[0])
                word = add_to_words_count(word, counter, False)
                if word is None:
                    continue
                edge_name = add_to_words_count(edge_name, counter, True)
                edges_list.append(NetworkXEdge(edge_name, word, counter))

    for edge in edges_list:
        output.write(edge.to_string()+'\n')

with open('report.txt', 'a', encoding='utf-8') as report:
    for r, v in replacements.items():
        report.write(f'Replacing {r} with {v}\n')
    for ex in expressions:
        report.write(f'Found expression: {ex}\n')
    for sp in special_answers:
        report.write(f'Removing special answer {sp}\n')



















