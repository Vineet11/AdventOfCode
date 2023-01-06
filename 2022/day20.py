import numpy as np
# mixed arr index holds index from the original array at current index so that mixed_sequence=input_msg[mixed_arr_index]

'''
Function to mix the input sequence according to algorithm
Input: sequence to be mixed
Returns: Sum of the i,j,k th element after 0
'''
def get_current_decrypted_seq(input_msg, mixed_idx):
        decrypted_seq =  np.zeros_like(input_msg)
        decrypted_seq[mixed_idx] = input_msg
        return decrypted_seq

def mix_sequence(input_msg, decryption_key = 1, num_mix = 1):
    msg_length = len(input_msg)
    decryption_key = decryption_key % (msg_length-1)
    print(decryption_key)
    # mixed arr index holds the position of input element in the mixed array
    # so that decrypted_message[mixed_arr[i]] = input_msg[i]
    mixed_arr_index = np.arange(msg_length)
    pos_zero = None
    # Every mixing of "val" at current index i, 
    # Target index = [i + val]
    # if target > source: indices between [source+1, target] are decremented by 1
    # if target < source: indices between [target, source-1] are incremented by 1
    # Order of mixing is followed from the original array
    for j in range(num_mix):
        for i in range(msg_length):
            curr_value = input_msg[i]
            if curr_value == 0:
                pos_zero = i
                # Use this to index mixed array at the end of the mixing process
            curr_value_sgn = (curr_value >=0)
            curr_value_abs = abs(curr_value)
            shift_value = ((curr_value_abs % (msg_length-1)) * decryption_key) % (msg_length-1)
            shift_value = shift_value if curr_value_sgn else -shift_value
            # shift_value = (curr_value % (msg_length-1)) if curr_value >= 0 else -((-curr_value) % (msg_length-1))
            curr_index = mixed_arr_index[i]
            if shift_value == 0:
                continue
            target_index = shift_value + curr_index
            # considering circular shifting
            # When the element wraps around, the target index is off by 1.
            # TODO: Not sure, how is wrapping around defined when the target is at 0 or n-1
            # for target=0, the input example says assume it moves back to the end 
            # keeping the same notion of n-1 as well
            if target_index > msg_length-1:
                target_index += 1
            elif target_index <= 0:
                target_index -= 1
            target_index = target_index % msg_length

            update, start_idx, end_idx = 0, 0, 0
            if target_index > curr_index :
                start_idx = curr_index + 1
                end_idx = target_index
                update = -1
            if target_index < curr_index :
                start_idx = target_index
                end_idx = curr_index - 1
                update = +1
            update_mask = (mixed_arr_index >= start_idx) & (mixed_arr_index <= end_idx)
            mixed_arr_index = mixed_arr_index + update * update_mask
            mixed_arr_index[i] = target_index
            # Debug prints:
            # print("after {}th iteration, curr_index is {}, curr value is {}, target_index is {}, position array is {}, mixed array is {}".format(i+1, curr_index, curr_value, target_index, mixed_arr_index, get_current_decrypted_seq(input_msg, mixed_arr_index)))
        if pos_zero is None:
            raise ValueError("Input message doesnt have zero value")
        pos_zero = mixed_arr_index[pos_zero]
        # print("after {}th mixing, the sequence is {}".format(j+1, get_current_decrypted_seq(input_msg, mixed_arr_index)))
    return get_current_decrypted_seq(input_msg, mixed_arr_index), pos_zero

def decrypt_sequence_pt1(input_msg):
    i = 1000
    j = 2000
    k = 3000
    decrpyted_seq, pos_zero = mix_sequence(input_msg)
    msg_len = len(input_msg)
    x = decrpyted_seq[(pos_zero+i) % msg_len]
    y = decrpyted_seq[(pos_zero+j) % msg_len]
    z = decrpyted_seq[(pos_zero+k) % msg_len]
    # print(pos_zero, decrpyted_seq)
    # print(x, y, z)
    return x+y+z

def decrypt_sequence_pt2(input_msg):
    i = 1000
    j = 2000
    k = 3000
    decryption_key = 811589153
    num_mix = 10
    decrpyted_seq = None,
    pos_zero = 0
    decrpyted_seq, pos_zero = mix_sequence(input_msg, decryption_key, num_mix)
    # print("after {}th mixing, the sequence is {}".format(i+1, decrpyted_seq))
    # prev_msg = decrpyted_seq
    msg_len = len(input_msg)
    x = decrpyted_seq[(pos_zero+i) % msg_len]
    y = decrpyted_seq[(pos_zero+j) % msg_len]
    z = decrpyted_seq[(pos_zero+k) % msg_len]
    print(pos_zero, decrpyted_seq[pos_zero])

    return np.int64(x+y+z)*np.int64(decryption_key)

def parse_input(filename):
    parsed_input=[]
    with open(filename, "r") as f:
        new_line = f.readline()
        while new_line:
            parsed_input.append(int(new_line.strip("\n")))
            new_line = f.readline()
    return np.array(parsed_input)

if __name__=="__main__":
    input_file = "20_1_input.txt"
    encrypted_message = parse_input(input_file)
    # encrypted_message = np.array([1, 2, -3, 3, -2, 0, 4])
    decrypted_message = decrypt_sequence_pt1(encrypted_message)
    print("answer for part 1 is {}".format(decrypted_message))
    decrypted_message = decrypt_sequence_pt2(encrypted_message)
    print("answer for part 2 is {}".format(decrypted_message))
