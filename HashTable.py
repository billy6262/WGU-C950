class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for x in range(size)]

    def insert(self, key, item):
        hash_value = hash(key) % self.size  #hashing the key value
        bucket = self.table[hash_value]     #calling the bucket of the hashed key
        i = 0
        while i < len(bucket):     #linear probing for collisions
            if bucket[i] == key:   #checking the key matches
                bucket[i + 1] = item #if key matches, update the item
                i = 1              #asing the index to a value to indicate successful update
                return
            i += 2
        if  i != 1: #checking if update succeeded
            bucket.append(key) #if not, append the item to the bucket
            bucket.append(item)

    def retrieve(self, key):
        hash_value = hash(key) % self.size
        bucket = self.table[hash_value]
        i = 0
        while i < len(bucket):
            print(key + " and " + i)
            if bucket[i] == key:
                return bucket[i + 1]
            i += 2
    
    def delete(self, key):
        hash_value = hash(key) % self.size
        bucket = self.table[hash_value]
        i = 0
        while i < len(bucket):
            if bucket[i] == key:
                del bucket[i]
                return
            i += 2
        