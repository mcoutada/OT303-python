import os
import xml.etree.ElementTree as ET

def parseDates(data):

    dates = []
    
    for i in data:
        date = i.attrib.get('CreationDate')[0:10]
        dates.append(date)

    return dates

def mapDates(data):

    data_dict = {}

    for i in data:
        if not i in data_dict.keys():
            data_dict[i] = 1
        else:
            data_dict[i] += 1
    
    return data_dict

def redDates(data):
    res = sorted(data, key = data.get, reverse = False)[:10]
    lowest_dates = {}

    for key in data:
        if key in res:
            lowest_dates[key] = data.get(key)
    
    return lowest_dates

if __name__ == '__main__':
    file_path = '/home/richarcos/Documentos/Stack Overflow 11-2010/112010 Meta Stack Overflow'
    tree = ET.parse(os.path.join(file_path, 'posts.xml'))
    root = tree.getroot()

    print(redDates(mapDates(parseDates(root))))
