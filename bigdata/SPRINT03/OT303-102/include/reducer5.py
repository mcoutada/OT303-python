import sys

# Reducer para: Relacion entre la cantidad de respuestas en un post y su puntaje
# (no era requerimiento mío, pero lo expusimos en el proyecto final así que lo hice)
# Si no entendí mal, no hay nada que reducir ya que se imprime una vez por post, así que es solo imprimir lo mapeado

# Print the header:
header = f"AnswerCount\tScore"
print(header)

for line in sys.stdin:
    print(line.strip())
