# Memory Module

## Overview
The `memory` module handles the storage, retrieval, and management of memories within the JarvisIRL system. It provides a centralized memory system for all neural networks.

## Classes

### Memory
- **`__init__(self, memory_file='memories.json')`**: Initializes the memory from a JSON file.
- **`load_memories(self)`**: Loads memories from the file.
- **`save_memories(self)`**: Saves memories to the file.
- **`add_memory(self, memory, strength=1)`**: Adds a new memory.
- **`get_memory(self, memory)`**: Retrieves a specific memory.
- **`update_memory(self, memory, strength)`**: Updates the strength of a memory.
- **`delete_memory(self, memory)`**: Deletes a memory.
- **`list_memories(self)`**: Lists all memories.
- **`clear_memories(self)`**: Clears all memories.
- **`update_memory_imprints(self, memories)`**: Updates memory imprints.
- **`retrieve_memories(self)`**: Retrieves all memories.
- **`save_memories_to_file(self, filepath)`**: Saves memories to a specific file.
- **`load_memories_from_file(self, filepath)`**: Loads memories from a specific file.

## Usage

### Initialization
```python
from memory import Memory

memory = Memory()
