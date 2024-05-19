import json
import threading
from typing import Any, Dict, List

class Memory:
    def __init__(self):
        self.memories: List[Dict[str, Any]] = []
        self.lock = threading.Lock()

    def store_memory(self, memory: Dict[str, Any]):
        with self.lock:
            self.memories.append(memory)

    def retrieve_memories(self) -> List[Dict[str, Any]]:
        with self.lock:
            return self.memories.copy()

    def clear_memories(self):
        with self.lock:
            self.memories.clear()

    def update_memory_imprints(self, memories: List[str], strength: int = 1):
        with self.lock:
            for memory in memories:
                existing_memory = next((m for m in self.memories if m['memory'] == memory), None)
                if existing_memory:
                    existing_memory['strength'] += strength
                else:
                    self.memories.append({'memory': memory, 'strength': strength})

    def save_memories_to_file(self, filepath: str):
        with self.lock:
            try:
                with open(filepath, 'w') as file:
                    json.dump(self.memories, file)
            except IOError as e:
                print(f"Error saving memories to file: {e}")

    def load_memories_from_file(self, filepath: str):
        with self.lock:
            try:
                with open(filepath, 'r') as file:
                    self.memories = json.load(file)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading memories from file: {e}")

# Example usage
if __name__ == "__main__":
    memory = Memory()
    memory.store_memory({'memory': 'example_memory_1', 'strength': 1})
    memory.store_memory({'memory': 'example_memory_2', 'strength': 2})

    print("Stored Memories:", memory.retrieve_memories())

    memory.update_memory_imprints(['example_memory_1', 'example_memory_3'], strength=2)

    print("Updated Memories:", memory.retrieve_memories())

    memory.save_memories_to_file('memories.json')
    memory.clear_memories()
    print("Cleared Memories:", memory.retrieve_memories())

    memory.load_memories_from_file('memories.json')
    print("Loaded Memories:", memory.retrieve_memories())
