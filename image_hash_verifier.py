import os
import hashlib

###########################################################################################
# The purpose of this script is to produce the image hash and provenance of the Swamp Stars
# art, making it possible for anyone to prove that the art has not changed from the initial
# deployment of the contract. This is important because it means that we cannot tamper with
# the art without it being known. 
#
# This script was used to generate the image hash data for all of the Swamp Stars and the
# final hash provenance from the combination of all of the image hashes. You can see the
# provenance hash in the contract by calling the _provenance() function. There is no way to
# change this value.
#
# The final provenance hash is the concatenation of the all of the Swamp Stars image hashes
# in their original order, NOT the final order after the shuffle. The original order can be 
# seen on the IPFS URI linked here: ipfs://0/
#
# Anyone can verify that the Swamp Stars have not been tampered with after the deployment
# by downloading the art from IPFS, running the art through this script, and comparing the
# result with the provenance on the contract. It would be nearly impossible for us to get
# the same provenance from the art if it has changed, given the nature and security of hash
# functions like SHA256.
#
# https://etherscan.io/address/0x712dc5238c226133be7cf4769de7f1794d37183f#readContract
###########################################################################################

# To prove the final provenenace you will need to download all 8,880 Swamp Stars, place them
# into a folder and make sure they are in the correct order.
#
# If you just want the hash value of a particular piece, then only have that one in the folder
# or the result won't be correct, but feel free to mess around with the script.

# Point this variable to the folder you are keeping the Swamp Stars art in
image_folder_path = "C:/please/replace/with/real/path/SwampStars/"
files = os.listdir(image_folder_path)

# in case you downloaded the IPFS folder as a whole and still have the _provenance file in there
if "_provenance" in files:
    files.remove("_provenance")

# sort the files them alphanumerically
files.sort(key=lambda x: int(os.path.splitext(x)[0]))

# a variable to store the full hash string
concat_hash_string = ""

for file in files:
    with open(image_folder_path + file,"rb") as f:
        bytes = f.read() # read entire image file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest() # convert image data to a hash string
        concat_hash_string += readable_hash # concatenate the hash

# dont need to take the hash if you only gave in one file since that files hash is already in there
if len(files) > 1:
    concat_hash_string = hashlib.sha256(concat_hash_string.encode('utf-8')).hexdigest()

print(concat_hash_string)
