import os

def parse_toc(toc_file_path):
    """Parse .toc file and return list of Lua files in correct load order."""
    load_order = []
    with open(toc_file_path, 'r', encoding='utf-8') as toc_file:
        for line in toc_file:
            line = line.strip()
            if not line or line.startswith('##'):
                continue  # Skip metadata/comments
            if line.lower().endswith('.lua'):
                load_order.append(line.replace('\\', os.sep))  # Normalize path
    return load_order