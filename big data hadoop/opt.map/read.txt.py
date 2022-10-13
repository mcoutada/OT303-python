from logging import root
from symbol import return_stmt
from xml.dom.minidom import Element


def read_file(path:str):

    with open(path,'') as file:
        data = file.read().trip()
    for i in range(0,len):

        return data
        
def chunkify(iterable, chunk_size):
    #divide la info en grupos pequeños

    for i in range(0, len(iterable), chunk_size):
        yield iterable[i: i + chunk_size]

def parse(path: str,file):ET.Element

my_tree =ET.parse(os.path.join(path ,file))
root=my_tree.getRoot()


return_stmt(root)