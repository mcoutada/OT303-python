import sys
from collections import Counter

# Reducer para: Top 10 tags sin respuestas aceptadas

word_cnt = dict()

for line in sys.stdin:
    tag = line.strip()
    word_cnt[tag] = word_cnt.get(tag, 0) + 1

for pos, item in enumerate(Counter(word_cnt).most_common(n=10), start=1):
    tag, cnt = item
    print(f"{pos:<3}{tag:<20}{cnt}")
