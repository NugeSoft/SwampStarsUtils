import hashlib
import json

#########################################################################################
# This script was used to shuffle the Swamp Stars using a random seed from Chainlink VRF.
#
# The purpose this scheme was so that no one, especially us, can know what Swamp Stars
# they would get before the VRF returns the seed, giving everyone a fair shot at minting.
#
# Anyone can verify that the Swamp Stars were ordered according to this scheme by getting
# the random seed we used from the contract with the function getRandomIndex() and then
# running it through the same functions used in this script. There is no way to change
# the random index after it has been set.
#
# https://etherscan.io/address/0x712dc5238c226133be7cf4769de7f1794d37183f#readContract
#########################################################################################


# We're using a Fisher-Yates shuffle algorithm with the random seed from Chainlink VRF.
# In simple terms, it takes a random item from a list and swaps it with the last item
# in the list that hasn't already been swapped. It repeats this swapping action until 
# it has iterated over every item in the list.
# For more details https://en.wikipedia.org/wiki/Fisher–Yates_shuffle
#
# The one big difference from a normal implementation of this algorithm is the reuse
# of the previous random number to generate the next, the purpose of which is to make
# the outcome deterministic and replicable but still unpredictable until we have the seed.
def randomize (array, n, startIndex):
    # have a variable hold the current random index so it can be reset
    random_index = startIndex

    # loop through array from last to first
    for i in range(n-1,0,-1):
        # Rather than using a known noise library or rng with a seed, we decided to use SHA256 to
        # generate pseudorandom numbers since it will be the easiest to prove for the user in the future.

        # convert the random index to a string and encode it into bytes
        byte_input = str(random_index).encode()

        # feed the bytes into the SHA256 hashing function
        hash_object = hashlib.sha256(byte_input)

        # read output as hex
        hash_val = hash_object.hexdigest()

        # convert back to a number which is really really big
        hash_result = int(hash_val, 16)

        # modulo the hash result by the total number of unswapped items to get the random index
        random_index = hash_result % (i+1)
        
        # Swap the item at the random index with the last unswapped item in the list
        array[i],array[random_index] = array[random_index],array[i]

    return array

# setting initial variables
VRF_random_seed = 0
array = []
max = 8880

# create a list of indices from 1 to 8880, these will be reordered using the random number
for i in range(1,max+1):
    array.append(i)

# call our implementation of Fisher-Yates Shuffle on the indices to reorder them
randomize(array,max,VRF_random_seed)

# printing the array so you can see the results are in the same order as the metadata
print( array )

# writing as json for easier reading
result = [
    {
        "startingIndexVRF": 0,
    }
]
for index, value in enumerate(array):
    info = {
        "tokenId": index+1,
        "imageIndex": value,
    }
    result.append(info)

with open('_metadata_ordering.json', 'w') as outfile:
    json.dump(result, outfile, indent=4)