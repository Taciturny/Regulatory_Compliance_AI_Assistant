import json
import os

def convert_txt_to_json(input_file, output_file):
    """
    input: A text file, an output file
    return: Json format of input text ...
    

    function: Receive a .txt file and convert it to appropriate json format
    
    """
    input_path = os.path.join("documents", input_file)
    output_path = os.path.join("documents", output_file)
    sections = []
    with open(input_path, 'r', encoding='utf-8') as file:
        section = {}
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith("Section :"):
                if section:  
                    sections.append(section)
                section = {"Section": line.split(":", 1)[1].strip()}
            elif line.startswith("Id :"):
                section["Id"] = int(line.split(":", 1)[1].strip())
            elif line.startswith("Content :"):
                section["Content"] = line.split(":", 1)[1].strip()
            else:
                section["Content"] += " " + line  
        if section: 
            sections.append(section)
    
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(sections, json_file, indent=4, ensure_ascii=False)

    return section

# Example usage
result = convert_txt_to_json("ndpa.txt", "ndpa.json")
#print(result)
