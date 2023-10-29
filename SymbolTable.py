class HashTable:
    def __init__(self, size=1000):
        self.size = size
        self.table = [[] for _ in range(self.size)]
    
    def hash(self, key):
        return hash(key) % self.size
    
    def insert(self, key, value):
        index = self.hash(key)
        for item in self.table[index]:
            if item[0] == key:
                item[1] = value  
                return
        self.table[index].append([key, value])
    
    def get(self, key):
        index = self.hash(key)
        for kv in self.table[index]:
            if kv[0] == key:
                return kv[1]
        return None 
    
    def delete(self, key):
        index = self.hash(key)
        for i, item in enumerate(self.table[index]):
            if item[0] == key:
                self.table[index].pop(i)
                return
            
    def contains(self, key):
        index = self.hash(key)
        for kv in self.table[index]:
            if kv[0] == key:
                return True
        return False        

class SymbolTable:
    def __init__(self):
        self.identifiers = HashTable()
    
    def insert(self, key, value):
        self.identifiers.insert(key, value)
    
    def get(self, key):
        return self.identifiers.get(key)
    
    def delete(self, key):
        self.identifiers.delete(key)

    def contains(self, key):
        return self.identifiers.contains(key)    