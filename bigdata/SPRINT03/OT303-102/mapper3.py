# import sys because we need to read and write data to STDIN and STDOUT
import sys
import xml.etree.ElementTree as ET

# Mapper para: Puntaje promedio de las repuestas con mas favoritos


posts_dic = dict()

# input comes from STDIN (standard input)
for line in sys.stdin:

    # 'PostTypeId="2"'  --> It's an answer
    # 'FavoriteCount' in line --> Just making sure it has a FavoriteCount, it should, this might not be needed...
    if 'PostTypeId="2"' in line and 'FavoriteCount="' in line:
        mapped = ET.fromstring(line)
        post_id = mapped.attrib["Id"]
        fav_cnt = float(mapped.attrib["FavoriteCount"])
        score = float(mapped.attrib["Score"])
        prev_fav_cnt, prev_score = posts_dic.get(post_id, (0, 0))
        if fav_cnt > prev_fav_cnt:
            posts_dic[post_id] = (fav_cnt, score)

# write the results to STDOUT (standard output);
# what we output here will be the input for the
# Reduce step, i.e. the input for reducer.py
for key in posts_dic:
    print(posts_dic[key][1])
