
from collections import deque

def index_in_array(array, car):
    """Returns the index of the last occurence of car in array"""
    return len(array) - list(array)[::-1].index(car) - 1 if car in array else -1

def indices(car, array):
    """Returns a list of all of the indices of car in array"""
    indices = []
    array = list(array)
    offset = 0
    while car in array:
        index = array.index(car)
        indices.append(index + offset)
        offset += index + 1
        array = array[index+1:]
    return indices


def seq_in_array(seq, array):
    ind = indices(seq[0], array)
    if not ind: return 0, 0
    
    array = list(array)
    longest_match = 0
    matching_index = 0
    for i in ind:
        match_size = 0
        for car1, car2 in zip(seq, array[i:]):
            if car1 == car2:
                match_size += 1
            else:
                break
        if match_size >= longest_match:
            longest_match = match_size
            matching_index = i
    return matching_index, longest_match
    

def lzss(text, search_buffer_size, look_ahead_buffer_size):
    search_buffer = deque([], maxlen=search_buffer_size)
    look_ahead_buffer = deque([], maxlen=look_ahead_buffer_size)
    output = ""
    
    i = 0
    for car in text:
        look_ahead_buffer.append(car)
        
        print(search_buffer, look_ahead_buffer)

        if car in search_buffer:
            index, length = seq_in_array(look_ahead_buffer, search_buffer)
            offset = i - index
            output += f"({offset},{length})"
            i += length
            
            for _ in range(index):
                search_buffer.append(look_ahead_buffer.pop())
        else:
            output += car
            search_buffer.append(car)
            i += 1
            
    return output

print(lzss("repetitive repeat", 11, 4))