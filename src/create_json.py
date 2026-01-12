import json
import os

def convert_txt_to_json(input_file, output_file):
    """
    Convert a text file to JSON format.
    
    This function reads a text file where each section is separated by a newline,
    and converts it to a JSON format. Each section in the text file should start
    with 'Section :', followed by 'Id :' and 'Content :'. The function will create
    a JSON object for each section with keys 'Section', 'Id', and 'Content'.
    
    Args:
    - input_file (str): The name of the input text file.
    - output_file (str): The name of the output JSON file.
    
    Returns:
    - dict: The last section converted to a dictionary, or an empty dictionary if no sections were found.
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
