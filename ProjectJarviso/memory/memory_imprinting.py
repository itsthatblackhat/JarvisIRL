# memory/memory_imprinting.py
import logging
from typing import List
from memory.memory import Memory

class MemoryImprinting:
    def __init__(self, memory):
        self.memory = memory

    def imprint_memory(self, new_memory):
        existing_memory = self.memory.get_memory(new_memory)
        if existing_memory:
            new_strength = existing_memory['strength'] + 1
            self.memory.update_memory(new_memory, new_strength)
            logging.info(f"Imprinted memory: {new_memory}. New strength: {new_strength}")
        else:
            self.memory.add_memory(new_memory, strength=1)
            logging.info(f"Imprinted new memory: {new_memory}")

    def retrieve_memories(self, threshold: int = 0) -> List[str]:
        return [memory['memory'] for memory in self.memory.memories if memory['strength'] >= threshold]

    def clear_weak_memories(self, threshold: int = 0):
        self.memory.memories = [memory for memory in self.memory.memories if memory['strength'] >= threshold]
        self.memory.save_memories()
        logging.info(f"Cleared weak memories with strength below {threshold}")

    def save_memories_to_file(self, filepath: str):
        self.memory.save_memories_to_file(filepath)

    def clear_memories(self):
        self.memory.clear_memories()

    def load_memories_from_file(self, filepath: str):
        self.memory.load_memories_from_file(filepath)
