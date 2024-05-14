# memory_imprinting.py
from memory import Memory

class MemoryImprinting(Memory):
    def __init__(self):
        super().__init__()
        self.memories = self.memories

    def imprint_memory(self, memory, strength):
        if memory in self.memories:
            index = self.memories.index(memory)
            self.memories[index]['strength'] += strength
        else:
            self.memories.append({'memory': memory, 'strength': strength})

    def retrieve_memories(self, threshold=0):
        relevant_memories = [memory['memory'] for memory in self.memories if memory['strength'] >= threshold]
        return relevant_memories

    def clear_weak_memories(self, threshold=0):
        self.memories = [memory for memory in self.memories if memory['strength'] >= threshold]