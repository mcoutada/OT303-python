import sys

# Reducer para: Relación entre cantidad de palabras en un post y su cantidad de respuestas
# (no era requerimiento mío, pero lo expusimos en el proyecto final así que lo hice)
# Si no entendí mal, no hay nada que reducir ya que se imprime una vez por post, así que es solo imprimir lo mapeado

# Print the header:
header = f"WordCount\tAnswerCount"
print(header)

for line in sys.stdin:
    print(line.strip())
