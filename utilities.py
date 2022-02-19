
'''
Yams
'''
import yaml

def yaml_loader(filepath):
    with open(filepath, "r") as file:
        yams = yaml.safe_load(file)
    return yams