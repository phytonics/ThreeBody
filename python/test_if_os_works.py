import os

file_path = os.path.dirname(os.path.realpath(__file__))
print(file_path)
parent_dir = "\\".join(file_path.split("\\")[:-1])
print(parent_dir)
