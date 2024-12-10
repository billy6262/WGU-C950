class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for x in range(size)]

    def insert(self, key, item):
        key = str(key)
        hash_value = hash(key) % self.size  #hashing the key value
        bucket = self.table[hash_value]     #calling the bucket of the hashed key
        if len(bucket) == 0:   #if bucket is empty, append the key and item
            bucket.append(key) #if not, append the item to the bucket
            bucket.append(item)
            return
        i = 0
        while i < len(bucket):     #linear probing for collisions
            if bucket[i] == key:   #checking the key matches
                bucket.insert(i + 1,item) #if key matches, update the item
                return
            i += 2

    def retrieve(self, key):
        key = str(key)
        hash_value = hash(key) % self.size 
        bucket = self.table[hash_value]
        i = 0
        while i < len(bucket):
            if bucket[i] == key:
                return bucket[i + 1]
            i += 1
    
    def delete(self, key):
        key = str(key)
        hash_value = hash(key) % self.size
        bucket = self.table[hash_value]
        i = 0
        while i < len(bucket):
            if bucket[i] == key:
                del bucket[i]
                return
            i += 2
        