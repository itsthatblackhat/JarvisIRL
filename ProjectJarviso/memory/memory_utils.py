import json

def preprocess_text(text):
    # Preprocess text data before storing in memory
    # For example, convert text to lowercase, remove punctuation, etc.
    processed_text = text.lower().strip()
    processed_text = processed_text.replace('.', '').replace(',', '')  # Remove punctuation
    return processed_text

def calculate_similarity(memory1, memory2):
    # Calculate similarity between two memories
    # For example, using cosine similarity, Jaccard similarity, etc.
    # Here, we assume both memories are strings and calculate Jaccard similarity
    memory1_set = set(memory1.split())
    memory2_set = set(memory2.split())
    intersection = len(memory1_set.intersection(memory2_set))
    union = len(memory1_set.union(memory2_set))
    similarity = intersection / union if union != 0 else 0
    return similarity

def save_to_file(filepath: str, data):
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file)
    except IOError as e:
        print(f"Error saving to file: {e}")

def load_from_file(filepath: str):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading from file: {e}")
        return None

# Example usage
if __name__ == "__main__":
    data = {'example_key': 'example_value'}
    save_to_file('example.json', data)

    loaded_data = load_from_file('example.json')
    print("Loaded Data:", loaded_data)
