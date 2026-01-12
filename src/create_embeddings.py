# Import necessary libraries
import json
import os
from sentence_transformers import SentenceTransformer


def generate_embeddings(json_file, output_file, model_name="all-MiniLM-L6-v2"):
    """
    INPUT:  json_file The Text data Without Embedding
            output_file The Text file to be created including embeddings
            model_name The sentence transformer file to be use for embedding

            Return NONE

            Function: Concatenate both section and question and return a json file 
            Including their embeddings
    """
    model = SentenceTransformer(model_name)
    input_path = os.path.join("documents", json_file)
    output_path = os.path.join("documents", output_file)
    
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for section in data:
        text_for_embedding = f"{section['Section']}: {section['Content']}"
        section["Embedding"] = model.encode(text_for_embedding).tolist()

    print(len(section["Embedding"]))
    
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Example usage
generate_embeddings("output.json", "content_section_embeddings.json")