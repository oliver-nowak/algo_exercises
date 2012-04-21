# Goal
# using the provided file of integers, find out if the 9 target sums are viable.
# print '0' if it is not viable, print '1' if it is viable

# 9 target sums:
# 231552, 234756, 596873, 648219,726312, 981237, 988331, 1277361, 1283379



target_list = [231552, 234756, 596873, 648219,726312, 981237, 988331, 1277361, 1283379]


hash_table = {}
with open("./data/Hashint.txt", "r") as f:
    for line in f:
        line = line.strip('\r\n')
        key_value = int(line)
        hash_table[ key_value ] = key_value 
            
bit_field = []
for target in target_list:
    
    is_valid = False
    for val_a in hash_table:
        # get the complementary value that makes up the target sum
        val_b = target - val_a

        # check if the complementary value is a valid key
        if val_b in hash_table:
            is_valid = True
            break
    
    if is_valid:
        bit_field.append(1)
    else:
        bit_field.append(0)


print '> ', bit_field
