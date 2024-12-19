class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for x in range(size)]  #table is intilized with a empty bucket(array) in each index

    def insert(self, key, item):
        key = str(key)
        hash_value = hash(key) % self.size  #hashing the key value
        bucket = self.table[hash_value]     #calling the bucket of the hashed key
        if len(bucket) == 0:   #if bucket is empty, append the key and item
            bucket.append(key) #if not, append the item to the bucket
            bucket.append(item)
            return True
        i = 0
        while i < len(bucket):     #linear probing for collisions
            if bucket[i] == key:   #checking the key matches
                bucket.insert(i + 1,item) #if key matches, update the item
                return True
            i += 2
        else: #if bucket has content but not the item match to the key, append
            bucket.append(key)
            bucket.append(item)
            return True

    def retrieve(self, key):
        key = str(key)
        hash_value = hash(key) % self.size 
        bucket = self.table[hash_value]
        i = 0
        while i < len(bucket):          #linear probing for key matches
            if bucket[i] == key:
                return bucket[i + 1]
            i += 2

    def retrieve_distances(self, adress1, adress2): #distance key are the hashed addresses. this function returns the same distance reguardless of the order the addresses are inserted. 
        key = f"{adress1}{adress2}"
        Rkey = f"{adress2}{adress1}"
        hash_value = hash(key) % self.size 
        Rhash_value = hash(Rkey) % self.size 
        bucket = self.table[hash_value]
        Rbucket = self.table[Rhash_value]
        i = 0
        while i < len(bucket):
            if bucket[i] == key:
                return bucket[i + 1]
            i += 1
        i = 0
        while i < len(Rbucket):
            if Rbucket[i] == Rkey:
                return Rbucket[i + 1]
            i += 1
    
    def delete(self, key):
        key = str(key)
        hash_value = hash(key) % self.size
        bucket = self.table[hash_value]
        i = 0
        while i < len(bucket):
            if bucket[i] == key:
                del bucket[i]
                return True
            i += 2
        return False
        
    def getBucket(self, key):
        key = str(key)
        hash_value = hash(key) % self.size
        return self.table[hash_value]