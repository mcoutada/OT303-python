import sys
from collections import Counter

# Reducer para: Puntaje promedio de las repuestas con mas favoritos

scores_sum = 0
scores_cnt = 0

for line in sys.stdin:
    scores_sum += float(line.strip())
    scores_cnt += 1


print(f"Average answers with more favorites: {scores_sum/scores_cnt}")
