import threading
from typing import List
from memory.memory import Memory

class MemoryImprinting:
    def __init__(self, memory_instance: Memory):
        self.memory_instance = memory_instance
        self.lock = threading.Lock()

    def imprint_memory(self, memory: str, strength: int):
        with self.lock:
            existing_memory = next((m for m in self.memory_instance.memories if m['memory'] == memory), None)
            if existing_memory:
                existing_memory['strength'] += strength
            else:
                self.memory_instance.memories.append({'memory': memory, 'strength': strength})
            self.memory_instance.save_memories()

    def retrieve_memories(self, threshold: int = 0) -> List[str]:
        with self.lock:
            return [memory['memory'] for memory in self.memory_instance.memories if memory['strength'] >= threshold]

    def clear_weak_memories(self, threshold: int = 0):
        with self.lock:
            self.memory_instance.memories = [memory for memory in self.memory_instance.memories if memory['strength'] >= threshold]
            self.memory_instance.save_memories()

    def save_memories_to_file(self, filepath: str):
        with self.lock:
            self.memory_instance.save_memories_to_file(filepath)

    def clear_memories(self):
        with self.lock:
            self.memory_instance.clear_memories()

    def load_memories_from_file(self, filepath: str):
        with self.lock:
            self.memory_instance.load_memories_from_file(filepath)
