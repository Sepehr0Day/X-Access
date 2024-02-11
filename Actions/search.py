import os, psutil
def search_file(filename):
    result_dict = {}
    partitions = [partition.mountpoint for partition in psutil.disk_partitions()]

    for partition in partitions:
        for root, dirs, files in os.walk(partition):
            if filename in files:
                file_path = os.path.join(root, filename)
                result_dict[file_path] = os.path.getsize(file_path)

    return result_dict