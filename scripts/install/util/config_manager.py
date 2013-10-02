import os


def get_local(filename, property_name):
    env = _read_file(filename)

    for l in env:
        if property_name in l:
            return l.split('=')[1].rstrip()  # Removing last "\n" char

    return None


def set_local(filename, property_name, value):
    with open(filename, 'r') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        if 'DNS' in lines[i]:
            lines[i] = 'DNS=' + value + '\n'

    with open(filename, 'w') as f:
        f.writelines(lines)


def load_into_os_environment(filename):
    env = _read_file(filename)

    print env

    for var in env:
        if '=' not in var:
            # Allowing empty lines
            continue

        (key, value) = var.split("=")
        os.environ[key] = value.rstrip()  # Removing last "\n" char


def _read_file(filename):
    with open(filename, 'r') as f:
        return f.readlines()
