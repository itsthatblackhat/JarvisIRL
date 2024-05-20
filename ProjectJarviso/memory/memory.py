import json
import logging
from pathlib import Path

class Memory:
    def __init__(self, memory_file='memories.json'):
        self.memory_file = Path(memory_file)
        self.memories = self.load_memories()

    def load_memories(self):
        if not self.memory_file.exists():
            logging.warning(f"{self.memory_file} does not exist. Starting with an empty memory.")
            return []
        with open(self.memory_file, 'r') as file:
            try:
                memories = json.load(file)
                logging.info(f"Loaded memories from {self.memory_file}")
                return memories
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON from {self.memory_file}: {e}")
                return []

    def save_memories(self):
        with open(self.memory_file, 'w') as file:
            json.dump(self.memories, file, indent=4)
        logging.info(f"Saved memories to {self.memory_file}")

    def add_memory(self, memory, strength=1):
        self.memories.append({"memory": memory, "strength": strength})
        self.save_memories()
        logging.info(f"Added memory: {memory} with strength: {strength}")

    def get_memory(self, memory):
        for mem in self.memories:
            if mem["memory"] == memory:
                return mem
        return None

    def update_memory(self, memory, strength):
        for mem in self.memories:
            if mem["memory"] == memory:
                mem["strength"] = strength
                self.save_memories()
                logging.info(f"Updated memory: {memory} to strength: {strength}")
                return True
        return False

    def delete_memory(self, memory):
        for mem in self.memories:
            if mem["memory"] == memory:
                self.memories.remove(mem)
                self.save_memories()
                logging.info(f"Deleted memory: {memory}")
                return True
        return False

    def list_memories(self):
        return self.memories

    def clear_memories(self):
        self.memories = []
        self.save_memories()
        logging.info("Cleared all memories")

    def save_memories_to_file(self, filepath):
        try:
            with open(filepath, 'w') as file:
                json.dump(self.memories, file, indent=4)
            logging.info(f"Saved memories to {filepath}")
        except Exception as e:
            logging.error(f"Error saving memories to {filepath}: {e}")

    def load_memories_from_file(self, filepath):
        try:
            with open(filepath, 'r') as file:
                self.memories = json.load(file)
            logging.info(f"Loaded memories from {filepath}")
        except Exception as e:
            logging.error(f"Error loading memories from {filepath}: {e}")
