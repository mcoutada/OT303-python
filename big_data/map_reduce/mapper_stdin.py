import sys
#from utils import read_file


def map(words: list[str]):
    with open('./map.txt', 'w') as f:
        for word in words:
            f.write(f'{word}\t{1}\n')


def map_stdin():
    for line in sys.stdin:
        words = line.split()
        # Count
        for word in words:
            # Write key-value to be processed by reducer.
            print(f'{word}\t{1}')


if __name__ == '__main__':
    #list_words = read_file('./file.txt').split()
    # map(list_words)
    map_stdin()
