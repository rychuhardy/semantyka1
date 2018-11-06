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

with open(outfile, 'a', encoding='utf-8') as output:
    for filename in filenames:
        with open(directory_name + filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            parsed_list = list(reader)
            for item in parsed_list:
                edge_name = filename.replace('.csv', '')
                edges_list.append(NetworkXEdge(edge_name, item[1], item[0]))

    for edge in edges_list:
        output.write(edge.to_string()+'\n')

