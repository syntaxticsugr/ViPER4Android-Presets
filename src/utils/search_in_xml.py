import xml.etree.ElementTree as ET
from pathlib import Path



def search_in_xml(xml: Path, key: str):
    tree = ET.parse(xml)
    root = tree.getroot()

    for elem in root.findall('.//'):
        if elem.get('name') == key:
            return elem.text or elem.get('value')

    return None
