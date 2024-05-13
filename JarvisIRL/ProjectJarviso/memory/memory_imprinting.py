# memory_imprinting.py
from memory import Memory

class MemoryImprinting(Memory):
    def __init__(self):
        super().__init__()

    def imprint_memory(self, memory, strength):
        # Check if the memory already exists
        if memory in self.memories:
            # If so, update its strength
            index = self.memories.index(memory)
            self.memories[index]['strength'] += strength
        else:
            # Otherwise, add the memory with the given strength
            self.memories.append({'memory': memory, 'strength': strength})

    def retrieve_memories(self, threshold=0):
        # Retrieve memories with a strength above the threshold
        relevant_memories = [memory['memory'] for memory in self.memories if memory['strength'] >= threshold]
        return relevant_memories

    def clear_weak_memories(self, threshold=0):
        # Clear memories with a strength below the threshold
        self.memories = [memory for memory in self.memories if memory['strength'] >= threshold]
