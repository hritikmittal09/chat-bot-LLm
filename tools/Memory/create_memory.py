import json
memory = dict()
import os
BASE_DIR = os.path.dirname(__file__)
MEMORY_PATH = os.path.join(BASE_DIR, "Memory.json")

def load_memory():
    global memory
    with open(MEMORY_PATH) as f :
        memory = json.load(f)
       # print(memory)


def get_memory(key):
    global memory
    load_memory()
    return memory[key]


def memory_keys():
    load_memory()
    return list(memory.keys())

if __name__ == "__main__" :
    #get_memory()
    print(get_memory("first_chatting"))


      


