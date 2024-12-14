import hashlib
import random

class CuckooFilter:
    def __init__(self, size=1024, bucket_size=4, max_kicks=500):
        """
        Initialize a Cuckoo Filter
        """
        self.size = size
        self.bucket_size = bucket_size
        self.max_kicks = max_kicks
        
        self.table = [[] for _ in range(size)]  # Initialize the hash table as a list of buckets (each storing fingerprints)

    def _hash(self, item):
        """
        Generate a hash for an item using SHA-256
        """
        return int(hashlib.sha256(str(item).encode()).hexdigest(), 16)

    def _fingerprint(self, item):
        """
        Generate a fingerprint for an item
        """
        return self._hash(item) & 0xFF  # Use last 8 bits of hash as a fingerprint

    def _get_bucket_indexes(self, item):
        """
        Calculate two candidate bucket indexes for an item
        """
        h1 = self._hash(item) % self.size  # i1 = hash(item)
        f = self._fingerprint(item)
        h2 = h1 ^ (self._hash(f) % self.size)  # i2 = i1 XOR hash(f)
        return h1, h2

    def insert(self, item):
        """
        Insert an item into the Cuckoo Filter
        """
        f = self._fingerprint(item)  # Generate fingerprint
        i1, i2 = self._get_bucket_indexes(item)  # i1 = h(item), i2 = i1 XOR hash(f)

        if len(self.table[i1]) < self.bucket_size:  # Try to insert in either bucket if empty
            self.table[i1].append(f)
            return True
        if len(self.table[i2]) < self.bucket_size:
            self.table[i2].append(f)
            return True

        # Otherwise, relocate existing items
        i = random.choice([i1, i2])  # Randomly choose between two buckets

        for _ in range(self.max_kicks):  # Perform up to max_kicks relocations
            j = random.randint(0, len(self.table[i]) - 1)  # Randomly select entry to kick out
            f, self.table[i][j] = self.table[i][j], f

            i = i ^ (self._hash(f) % self.size)  # Calculate alternate bucket for the kicked out f
            if len(self.table[i]) < self.bucket_size:  # If the alternate bucket has space, insert f
                self.table[i].append(f)
                return True

        return False  # Table is considered full

    def delete(self, item):
        """
        Delete an item from the Cuckoo Filter
        """
        f = self._fingerprint(item)  # Generate fingerprint
        i1, i2 = self._get_bucket_indexes(item)  # i1 = h(item), i2 = i1 XOR hash(f)

        if f in self.table[i1]:  # Try to remove the fingerprint from either bucket
            self.table[i1].remove(f)
            return True
        if f in self.table[i2]:
            self.table[i2].remove(f)
            return True

        return False

    def load_factor(self):
        """
        Calculate the current load factor of the Cuckoo Filter
        """
        occupied_slots = sum(len(bucket) for bucket in self.table)  # Count occupied slots
        total_slots = self.size * self.bucket_size  # Calculate total slots
        return (occupied_slots / total_slots) * 100  # Return load factor percentage
    
    def __contains__(self, item):
        """
        Check probable membership
        """
        f = self._fingerprint(item)  # Generate fingerprint
        i1, i2 = self._get_bucket_indexes(item)  # i1 = h(item), i2 = i1 XOR hash(f)

        return f in self.table[i1] or f in self.table[i2]  # Check if buckets contain fingerprint
