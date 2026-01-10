def load_config(file_path='config.txt'):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            name, value = line.split('=', 1)
            config[name.strip()] = value.strip()
    return config
