class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for x in range(size)]  #table is initialized with a empty bucket(array) in each index

    def insert(self, key, item):
        skey = str(key)
        hash_value = hash(skey) % self.size  #hashing the key value
        bucket = self.table[hash_value]     #calling the bucket of the hashed key
        if len(bucket) == 0:   #if bucket is empty, append the key and item
            bucket.append(skey) #if not, append the item to the bucket
            bucket.append(item)
            return True
        i = 0
        while i < len(bucket):     #linear probing for collisions
            if bucket[i] == skey:   #checking the key matches
                bucket.insert(i + 1,item) #if key matches, update the item
                return True
            i += 1
        if i == len(bucket): #if bucket has content but not the item match to the key, append
            bucket.append(skey)
            bucket.append(item)
            return True

    def retrieve(self, key):
        skey = str(key)
        hash_value = hash(skey) % self.size 
        bucket = self.table[hash_value]
        i = 0
        while i < len(bucket): #linear probing
            if bucket[i] == skey:
                return bucket[i + 1]  #return the item
            i += 1

    def retrieve_distances(self, adress1, adress2): #distance key are the hashed addresses. this function returns the same distance regardless of the order the addresses are inserted. 
        key = f"{adress1}{adress2}"
        Rkey = f"{adress2}{adress1}"
        hash_value = hash(key) % self.size 
        Rhash_value = hash(Rkey) % self.size 
        bucket = self.table[hash_value]
        Rbucket = self.table[Rhash_value]


        i = 0
        while i < len(bucket):  #probing for the key
            if bucket[i] == key:
                return bucket[i + 1]
            i += 1
        i = 0
        while i < len(Rbucket): #probing for the reversed key
            if Rbucket[i] == Rkey:
                return Rbucket[i + 1]
            i += 1
    
    def delete(self, key):
        skey = str(key)
        hash_value = hash(skey) % self.size
        bucket = self.table[hash_value]
        i = 0
        while i < len(bucket):
            if bucket[i] == skey:
                del bucket[i]
                return True
            i += 1
        return False
        
    def getBucket(self, key):
        skey = str(key)
        hash_value = hash(skey) % self.size
        return self.table[hash_value]