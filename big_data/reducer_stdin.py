import sys


def reduce_stdin():
    """"Reduce function for hadoop using standar input.
    """

    current_item = None
    current_count = 0
    for line in sys.stdin:
        # Get key-value
        item, count = line.split("\t")

        try:
            count = int(count)
        except ValueError:
            continue

        if current_item == item:
            current_count += count  # 1

        else:
            if current_item:  # First iteration.
                print(f'{current_item}\t{current_count}')
            current_item = item
            current_count = count  # 1

    if current_item == item:  # Last iteration
        print(f'{current_item}\t{current_count}')


if __name__ == '__main__':
    reduce_stdin()
