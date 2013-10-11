import os


def config_path(role):
    return 'config/' + role + '.env'


def get_local(filename, property_name):
    env = _read_file(filename)

    for l in env:
        if property_name in l:
            return l.split('=')[1].rstrip()  # Removing last "\n" char

    return None


def set_local(filename, property_name, value):
    lines = _read_file(filename)

    for i in range(len(lines)):
        if property_name in lines[i]:
            lines[i] = property_name + '=' + value + '\n'

    _write_file(filename, lines)


def check_locals(filename):
    # Checks if all the variables are set
    env = _read_file(filename)
    res = True

    for l in env:
        var = l.split('=')
        if len(var) < 2 and len(var) > 0:
            print 'The variable ' + var[0] + ' is not set'
            res = False

    return res


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


def _write_file(filename, content):
    with open(filename, 'w') as f:
        f.writelines(content)
