import sys
import os
from datetime import datetime
import pandas as pd

# Reducer 2
# Relación entre cantidad de respuestas y sus visitas.


with open("views_answers.txt","w") as VA:
    file1 = open(f"newfile_mapped.txt","r")
    for line in file1:
        line = line.strip()
        line = line.split(" ")
        try:
            if line[3] and line[4] != 0: 
                VA.write("{} {}\n".format(line[4],line[3]))
        except:
            pass
