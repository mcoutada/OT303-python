import xml.etree.ElementTree as ET
import os


def read_file(path_to_file: str) -> list[str]:
    """Read file from path.
    Args:
        path_to_file (str): src to the txt file.
    Returns:
        list[str]: list of words.
    """

    with open(path_to_file, 'r') as file:
        data = file.read().strip()

    return data


def chunkify(iterable, chunk_size):
    """Chunk data in smallers groups.
    Args:
        iterable (dict,map,list,..): iterable object.
        chunk_size (int): size for chunk.
    Yields:
        array_data: batch of data.
    """
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i: i + chunk_size]


def parse(path: str, file: str) -> ET.Element:
    """Parse xml file and return the root.
    Args:
        path (str): src where file is saved.
    Returns:
        ET.Element: root parsed file.
    """
    my_tree = ET.parse(os.path.join(path, file))
    my_root = my_tree.getroot()
    return my_root
