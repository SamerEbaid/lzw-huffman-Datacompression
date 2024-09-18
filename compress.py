import os 

##########################
# Define a class to represent nodes in the Huffman tree
class Node:
    def __init__(self, freq, char=None):
        self.freq = freq
        self.char = char
        self.left = None
        self.right = None
        

# Function to create the Huffman tree given a list of character frequencies
def creat_tree(freq):
    # Create a leaf node for each character and assign its frequency as its weight
    nodes = [Node(freq=f[1], char=f[0]) for f in freq]
    
    # Build the Huffman tree by repeatedly combining the two nodes with the lowest weights
    while len(nodes) > 1:
        # Sort the nodes by weight
        nodes.sort(key=lambda x: x.freq)
        
        # Create a new internal node with a weight equal to the sum of the two lowest-weight nodes
        new_node = Node(freq=nodes[0].freq + nodes[1].freq)
        new_node.left = nodes.pop(0)
        new_node.right = nodes.pop(0)
        
        # Add the new node to the list of nodes
        nodes.append(new_node)
    
    # Return the root node of the Huffman tree
    return nodes[0] 

# Function to encode bit patterns to each character in the Huffman tree
def getcode(node, code='', code_dict=None):
    # If no code dictionary is provided, create a new dictionary
    if code_dict is None:
        code_dict = {}

    # Assign the bit pattern to the current node
    node.code = code
    
    # If the node represents a character, add it and its bit pattern to the dictionary
    if node.char:
        code_dict[node.char] = node.code
    # Otherwise, recursively assign bit patterns to the left and right child nodes
    else:
        getcode(node.left, code + '0', code_dict)
        getcode(node.right, code + '1', code_dict)
    
    # Return the dictionary
    return code_dict

# Function to decode a Huffman code using the character codes dictionary
def huffman_decompress(binary_file_path, code_dict, output_text_file_path):
    with open(binary_file_path, 'rb') as file:
        encoded_bytes = file.read()

    encoded_bits = ''.join(format(byte, '08b') for byte in encoded_bytes)
    decoded_text = ''
    current_code = ''

    for bit in encoded_bits:
        current_code += bit
        if current_code in code_dict.values():
            decoded_text += list(code_dict.keys())[list(code_dict.values()).index(current_code)]
            current_code = ''

    with open(output_text_file_path, 'w') as output_file:
        output_file.write(decoded_text)

# Read the input text file and count the frequency of each character
text_file1 = open("1260.txt","r")
string1 = text_file1.read()
text_file1.close()
###################################
text_file2 = open("1497.txt","r")
string2 = text_file2.read()
text_file2.close()
############################
text_file3 = open("30360-8.txt","r")
string3= text_file3.read()
text_file3.close()
##############################
frequ1 = {}
for x in string1:
    if x in frequ1:
        frequ1[x] += 1
    else:
        frequ1[x] = 1
###############################
frequ2 = {}
for x in string2:
    if x in frequ2:
        frequ2[x] += 1
    else:
        frequ2[x] = 1
####################################
frequ3 = {}
for x in string3:
    if x in frequ3:
        frequ3[x] += 1
    else:
        frequ3[x] = 1
####################################
# Sort the character frequencies in ascending order
#print(frequ1)
ffrequ1 = sorted(frequ1.items(), key=lambda x: x[1], reverse=False)
ffrequ2 = sorted(frequ2.items(), key=lambda x: x[1], reverse=False)
ffrequ3 = sorted(frequ3.items(), key=lambda x: x[1], reverse=False)
#print(frequ1)
# Create the Huffman tree and assign bit patterns to each character
root1 = creat_tree(ffrequ1)
code_dict1 = getcode(root1)
##print(code_dict)
###################################
root2 = creat_tree(ffrequ2)
code_dict2 = getcode(root2)
#####################################
root3 = creat_tree(ffrequ3)
code_dict3 = getcode(root3)
##############################################
# Encode the input text using the Huffman code
encoded_text1 = ''.join([code_dict1[char] for char in string1])
encoded_text2 = ''.join([code_dict2[char] for char in string2])
encoded_text3 = ''.join([code_dict3[char] for char in string3])

# Convert the binary-encoded text into bytes
encoded_bytes1 = bytes(int(encoded_text1[i:i+8], 2) for i in range(0, len(encoded_text1), 8))
encoded_bytes2 = bytes(int(encoded_text2[i:i+8], 2) for i in range(0, len(encoded_text2), 8))
encoded_bytes3 = bytes(int(encoded_text3[i:i+8], 2) for i in range(0, len(encoded_text3), 8))

# Write bytes to binary files
with open('file1_binary.bin', 'wb') as file:
    file.write(encoded_bytes1)

with open('file2_binary.bin', 'wb') as file:
    file.write(encoded_bytes2)

with open('file3_binary.bin', 'wb') as file:
    file.write(encoded_bytes3)

#############################################################
#calculate size 
file_size1 = (os.path.getsize('1260.txt'))*8
file_size2 = (os.path.getsize('1497.txt'))*8
file_size3 = (os.path.getsize('30360-8.txt'))*8
compr1=round(file_size1/len(encoded_text1),4)
compr2=round(file_size2/len(encoded_text2),4)
compr3=round(file_size3/len(encoded_text3),4)
print("Huffman")
print("File original Size of file 1 is :", file_size1, "bits","||File Size of file 1 after compression is :",len(encoded_text1),"bits")
print("File original Size of file 2 is :", file_size2, "bits","||File Size of file 2 after compression is :",len(encoded_text1),"bits")
print("File original Size of file 3 is :", file_size3, "bits","||File Size of file 3 after compression is :",len(encoded_text1),"bits")
####################################################################

#########################################################################################################################################
################################################################
def compress(text):
    dictionary = {chr(i): i for i in range(256)}
    result = []
    p = text[0]
    
    for c in text[1:]:
        pc = p + c
        if pc in dictionary:
            p = pc
        else:
            result.append(dictionary[p])
            dictionary[pc] = len(dictionary)
            p = c
    
    result.append(dictionary[p])
    return result

def decompress(compressed):
    dictionary = {i: chr(i) for i in range(256)}
    result = [dictionary[compressed[0]]]
    p = dictionary[compressed[0]]
    
    for code in compressed[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == len(dictionary):
            entry = p + p[0]
        else:
            raise ValueError("Invalid code: " + str(code))
        
        result.append(entry)
        dictionary[len(dictionary)] = p + entry[0]
        p = entry
    
    return ''.join(result)

# Test the LZW compression and decompression
file_name1 = "1260.txt"
with open(file_name1, "r") as file:
    text1 = file.read()
file_name2 = "1497.txt"
with open(file_name2, "r") as file:
    text2 = file.read()
file_name3 = "30360-8.txt"
with open(file_name3, "r") as file:
    text3 = file.read()

# Compress the text using LZW algorithm
compressed_result1 = compress(text1)
compressed_result2 = compress(text2)
compressed_result3 = compress(text3)

# Convert the compressed LZW data into bytes
# Convert the compressed LZW data into bytes (clamp values to the range 0 to 255)
compressed_bytes1 = bytes(min(max(code, 0), 255) for code in compressed_result1)
compressed_bytes2 = bytes(min(max(code, 0), 255) for code in compressed_result2)
compressed_bytes3 = bytes(min(max(code, 0), 255) for code in compressed_result3)


# Write compressed data to binary files
with open('file1_lzw.bin', 'wb') as file:
    file.write(compressed_bytes1)

with open('file2_lzw.bin', 'wb') as file:
    file.write(compressed_bytes2)

with open('file3_lzw.bin', 'wb') as file:
    file.write(compressed_bytes3)

#############################################################
comprl1=round(file_size1/len(compressed_result1),4)
comprl2=round(file_size2/len(compressed_result2),4)
comprl3=round(file_size3/len(compressed_result3),4)
print("LZW")
print("File original Size of file 1 is :", file_size1, "bits","||File Size of file 1 after compression is :",len(compressed_result1),"bits")
print("File original Size of file 2 is :", file_size2, "bits","||File Size of file 2 after compression is :",len(compressed_result2),"bits")
print("File original Size of file 3 is :", file_size3, "bits","||File Size of file 3 after compression is :",len(compressed_result3),"bits")

print("Huffman || file 1 || file 2 || file 3 ||")
print("        ||",compr1,"||",compr2,"||",compr3,"||")
print("------------------------------------------------")  
print("LZW     |",comprl1,"|",comprl2,"|",comprl3,"||")
print("------------------------------------------------")
#########################################################################################################################################


# Decompress using Huffman decompression and save to a text file

huffman_decompress('file1_binary.bin', code_dict1,'file1_decompressed_huffman.txt')
huffman_decompress('file2_binary.bin', code_dict2,'file2_decompressed_huffman.txt')
huffman_decompress('file3_binary.bin', code_dict3,'file3_decompressed_huffman.txt')
##############################################################################################################

output_texts = [decompress(compressed_result1),decompress(compressed_result2),decompress(compressed_result3)]
file_names = ['file1_decompressed_lzw.txt', "file2_decompressed_lzw.txt", "file3_decompressed_lzw.txt"]

for i, file_name in enumerate(file_names):
    with open(file_name, "w") as file:
        file.write(output_texts[i])
#####################################################################################################################
