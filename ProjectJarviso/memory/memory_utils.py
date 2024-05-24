# memory/memory_utils.py
import json
import logging

class MemoryUtils:
    @staticmethod
    def load_memory_from_file(file_path):
        try:
            with open(file_path, 'r') as file:
                memory_data = json.load(file)
                logging.info(f"Loaded memory data from {file_path}")
                return memory_data
        except FileNotFoundError:
            logging.error(f"Memory file {file_path} not found.")
            return {}
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from {file_path}: {e}")
            return {}

    @staticmethod
    def save_memory_to_file(file_path, memory_data):
        try:
            with open(file_path, 'w') as file:
                json.dump(memory_data, file, indent=4)
                logging.info(f"Saved memory data to {file_path}")
        except Exception as e:
            logging.error(f"Error saving memory data to {file_path}: {e}")

    @staticmethod
    def export_memories(memory_instance, export_file):
        try:
            with open(export_file, 'w') as file:
                json.dump(memory_instance.list_memories(), file, indent=4)
            logging.info(f"Exported memories to {export_file}")
        except Exception as e:
            logging.error(f"Failed to export memories: {e}")

    @staticmethod
    def import_memories(memory_instance, import_file):
        try:
            with open(import_file, 'r') as file:
                imported_memories = json.load(file)
                for memory in imported_memories:
                    memory_instance.add_memory(memory["memory"], memory["strength"])
            logging.info(f"Imported memories from {import_file}")
        except Exception as e:
            logging.error(f"Failed to import memories: {e}")

    @staticmethod
    def merge_memories(memory_instance_1, memory_instance_2):
        combined_memories = memory_instance_1.list_memories() + memory_instance_2.list_memories()
        memory_dict = {}
        for memory in combined_memories:
            if memory["memory"] in memory_dict:
                memory_dict[memory["memory"]] += memory["strength"]
            else:
                memory_dict[memory["memory"]] = memory["strength"]

        merged_memories = [{"memory": memory, "strength": strength} for memory, strength in memory_dict.items()]
        memory_instance_1.memories = merged_memories
        memory_instance_1.save_memories()
        logging.info("Merged memories from two instances")
        return merged_memories
