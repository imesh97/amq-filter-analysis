import bitarray
import hashlib

class BloomFilter:
    def __init__(self, size, num_hashes):
        """
        Initialize Bloom Filter
        """
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bitarray.bitarray(size)
        self.bit_array.setall(0)
        
    def _hash(self, item, seed):
        """
        Generate hash for item using SHA-256
        """
        hash_input = f"{seed}{item}".encode('utf-8')
        return int(hashlib.sha256(hash_input).hexdigest(), 16) % self.size
    
    def insert(self, item):
        """
        Insert item into Bloom Filter
        """
        for i in range(self.num_hashes):
            index = self._hash(item, i)
            self.bit_array[index] = True
    
    def __contains__(self, item):
        """
        Check probable membership
        """
        return all(
            self.bit_array[self._hash(item, i)] 
            for i in range(self.num_hashes)
        )
