import os

def get_local(file, property):
    env = _read_file(file)

    for l in env:
        if property in l:
            return l.split('=')[1].rstrip() # Removing last "\n" char

    return None

def set_local(file, property, value):
    with open(file, 'r') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        if 'DNS' in lines[i]:
            lines[i] = 'DNS=' + value + '\n'

    with open(file, 'w') as f:
        f.writelines(lines)

def load_into_os_environment(file):
    env = _read_file(file)

    print env

    for var in env:
        if '=' not in var:
            # Allowing empty lines
            continue

        (key, value) = var.split("=")
        os.environ[key] = value.rstrip()  # Removing last "\n" char


def _read_file(file):
    with open(file, 'r') as f:
        return f.readlines()