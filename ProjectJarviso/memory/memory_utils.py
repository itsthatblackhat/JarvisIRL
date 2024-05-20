import json
import logging

class MemoryUtils:
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
        merged_memories = []
        memory_dict = {}
        for memory in combined_memories:
            if memory["memory"] in memory_dict:
                memory_dict[memory["memory"]] += memory["strength"]
            else:
                memory_dict[memory["memory"]] = memory["strength"]
        for memory, strength in memory_dict.items():
            merged_memories.append({"memory": memory, "strength": strength})
        memory_instance_1.memories = merged_memories
        memory_instance_1.save_memories()
        logging.info("Merged memories from two instances")
