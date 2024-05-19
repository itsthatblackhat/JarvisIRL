from typing import List
from memory.memory import Memory

class MemoryImprinting(Memory):
    def __init__(self):
        super().__init__()

    def imprint_memory(self, memory: str, strength: int):
        with self.lock:
            existing_memory = next((m for m in self.memories if m['memory'] == memory), None)
            if existing_memory:
                existing_memory['strength'] += strength
            else:
                self.memories.append({'memory': memory, 'strength': strength})

    def retrieve_memories(self, threshold: int = 0) -> List[str]:
        with self.lock:
            return [memory['memory'] for memory in self.memories if memory['strength'] >= threshold]

    def clear_weak_memories(self, threshold: int = 0):
        with self.lock:
            self.memories = [memory for memory in self.memories if memory['strength'] >= threshold]

    def save_memories_to_file(self, filepath: str):
        with self.lock:
            super().save_memories_to_file(filepath)

    def clear_memories(self):
        with self.lock:
            super().clear_memories()

    def load_memories_from_file(self, filepath: str):
        with self.lock:
            super().load_memories_from_file(filepath)

# Example usage
if __name__ == "__main__":
    memory_imprinting = MemoryImprinting()
    memory_imprinting.imprint_memory('example_memory_1', 1)
    memory_imprinting.imprint_memory('example_memory_2', 2)

    print("Stored Memories:", memory_imprinting.retrieve_memories())

    memory_imprinting.imprint_memory('example_memory_1', 2)
    memory_imprinting.imprint_memory('example_memory_3', 1)

    print("Updated Memories:", memory_imprinting.retrieve_memories())

    memory_imprinting.clear_weak_memories(threshold=2)
    print("Cleared Weak Memories:", memory_imprinting.retrieve_memories())

    memory_imprinting.save_memories_to_file('imprinted_memories.json')
    memory_imprinting.clear_memories()
    print("Cleared Memories:", memory_imprinting.retrieve_memories())

    memory_imprinting.load_memories_from_file('imprinted_memories.json')
    print("Loaded Memories:", memory_imprinting.retrieve_memories())
