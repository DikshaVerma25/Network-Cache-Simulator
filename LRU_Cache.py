from collections import OrderedDict


class LRU_Cache:
    current_capacity = 0
    
    # initialising capacity
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.current_memory_used = 0
    
    def search(self, key: int) -> int:
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key,last=True)
            return self.cache[key]

   
    def put(self, file_id: int, file_size: int) -> None:
        while self.current_memory_used + file_size >= self.capacity:
            try:
                removed = self.cache.popitem(last=False)
                self.current_memory_used -= removed[1]
            except KeyError:
                return
        self.cache[file_id] = file_size
        self.current_memory_used += file_size
        self.cache.move_to_end(file_id)

    def print_contents(self):
        for key in self.cache:
            print("File_id : {} , file_size: {}".format(str(key), str(self.cache.get(key))))
