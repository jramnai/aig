import os


def _get_file_extension(file_name):
    return os.path.splitext(file_name)[1]
