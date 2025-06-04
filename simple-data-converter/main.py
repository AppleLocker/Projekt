import sys
import json
import yaml
import xml.etree.ElementTree as ET
from xml.dom import minidom

def json_to_dict(file_path):
    with open(file_path) as f:
        return json.load(f)

def yaml_to_dict(file_path):
    with open(file_path) as f:
        return yaml.safe_load(f)

def xml_to_dict(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return {root.tag: parse_xml_element(root)}

def parse_xml_element(element):
    if len(element) == 0:
        return element.text
    result = {}
    for child in element:
        child_data = parse_xml_element(child)
        if child.tag in result:
            if type(result[child.tag]) is list:
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag]], child_data
        else:
            result[child.tag] = child_data
    return result

def dict_to_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def dict_to_yaml(data, file_path):
    with open(file_path, 'w') as f:
        yaml.dump(data, f)

def dict_to_xml(data, file_path):
    root_name = next(iter(data))
    root = ET.Element(root_name)
    build_xml(root, data[root_name])
    
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    with open(file_path, 'w') as f:
        f.write(xmlstr)

def build_xml(parent, data):
    if isinstance(data, dict):
        for key, value in data.items():
            elem = ET.SubElement(parent, key)
            build_xml(elem, value)
    elif isinstance(data, list):
        for item in data:
            build_xml(parent, item)
    else:
        parent.text = str(data)

def convert_file(input_file, output_file):
    input_ext = input_file.split('.')[-1].lower()
    output_ext = output_file.split('.')[-1].lower()
    
    # Wczytaj dane
    if input_ext == 'json':
        data = json_to_dict(input_file)
    elif input_ext in ('yml', 'yaml'):
        data = yaml_to_dict(input_file)
    elif input_ext == 'xml':
        data = xml_to_dict(input_file)
    else:
        raise ValueError("Nieobsługiwany format wejściowy")
    
    # Zapisz dane
    if output_ext == 'json':
        dict_to_json(data, output_file)
    elif output_ext in ('yml', 'yaml'):
        dict_to_yaml(data, output_file)
    elif output_ext == 'xml':
        dict_to_xml(data, output_file)
    else:
        raise ValueError("Nieobsługiwany format wyjściowy")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Użycie: python main.py input_file output_file")
        sys.exit(1)
    
    try:
        convert_file(sys.argv[1], sys.argv[2])
        print("Konwersja zakończona sukcesem!")
    except Exception as e:
        print(f"Błąd: {str(e)}")
        sys.exit(1)