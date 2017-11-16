"""
sumarize.py
"""
import os


def read_details_allFiles(folder_name, file_name):
    fname = os.path.join(folder_name, file_name)
    with open(fname, 'r') as fp:
        File_details = fp.read()
    return File_details


def write_summary_file(file_details, file__write_details):
    with open('summary.txt', 'a') as fsw:
        fsw.write(file_details + '\n')
        fsw.write(file__write_details)


def main():
    collector_details = read_details_allFiles("Collect_Folder", "collector_details.txt")
    f = open('summary.txt', 'r+')
    f.truncate()
    write_summary_file("Collect.py Details ", collector_details)
    classify_details = read_details_allFiles("Classify_Folder", "classify_details.txt")
    write_summary_file("Classify.py Details ", classify_details)
    cluster_details = read_details_allFiles("Cluster_Folder", "cluster_details.txt")
    write_summary_file("Cluster.py Details ", cluster_details)

if __name__ == '__main__':
    main()