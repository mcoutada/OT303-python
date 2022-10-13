# import sys because we need to read and write data to STDIN and STDOUT
import sys
import xml.etree.ElementTree as ET

# Mapper para: Top 10 tags sin respuestas aceptadas


# input comes from STDIN (standard input)
for line in sys.stdin:

    # 'PostTypeId="1"'  --> It's a question
    # "AcceptedAnswerId" not in line --> the tag doesn't exist, it has no accepted answer
    if 'PostTypeId="1"' in line and "AcceptedAnswerId" not in line:

        mapped = ET.fromstring(line)
        tags_str = mapped.attrib["Tags"]
        for tag in tags_str.strip("<>").split("><"):
            # write the results to STDOUT (standard output);
            # what we output here will be the input for the
            # Reduce step, i.e. the input for reducer.py
            print(tag)
