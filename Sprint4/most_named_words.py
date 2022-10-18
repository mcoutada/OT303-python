import string
import xml.etree.ElementTree as ET
import re
import os

def parseBody(data):
    
    content = []

    tag_re = re.compile(r'<[^>]+>')
    link_re = re.compile(r'^https?:\/\/.*[\r\n]*')

    for i in data:
        post = link_re.sub('',
                            tag_re.sub('',
                            i.attrib.get('Body')))
        content.append(post)

    return content

def mapBody(data):

    freq_dict = {}

    for post in data:
        
        post = post.strip()

        post = post.lower()

        for val in string.punctuation:
            if val not in ("'"):
                post = post.replace(val,"")
        
        words = post.split(" ")

        for word in words:
            if not (word in freq_dict.keys()):
                freq_dict[word] = 1
            else:
                freq_dict[word] += 1
    
    return freq_dict

def reduceBody(data):
    
    res = sorted(data, key=data.get, reverse=True)[:10]
    max_words = {}

    for key in data:
        if key in res:
            max_words[key] = data.get(key)
    
    return max_words

if __name__ == '__main__':
    file_path = '/home/richarcos/Documentos/Stack Overflow 11-2010/112010 Meta Stack Overflow'
    tree = ET.parse(os.path.join(file_path, 'posts.xml'))
    root = tree.getroot()

    print(reduceBody(mapBody(parseBody(root))))
