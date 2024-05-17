def identify_problematic_bytes(file_path):
    problematic_bytes = []
    with open(file_path, 'rb') as file:
        byte = file.read(1)
        while byte:
            try:
                byte.decode('utf-8')
            except UnicodeDecodeError:
                problematic_bytes.append(byte)
            byte = file.read(1)
    return problematic_bytes

file_path = "BrainModel/Cleaned_Brainconv.obj"
problematic_bytes = identify_problematic_bytes(file_path)
print("Problematic bytes:", problematic_bytes)
