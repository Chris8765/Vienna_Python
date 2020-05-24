# Given the triangle of consecutive odd numbers:
#
#             1
#          3     5
#       7     9    11
#   13    15    17    19
#21    23    25    27    29
#...
#Calculate the row sums of this triangle from the row index (starting at index 1) e.g.:
#
#row_sum_odd_numbers(1); # 1
#row_sum_odd_numbers(2); # 3 + 5 = 8


n = int(input("Give your row: "))
def row_sum_odd_numbers(n):
    if n == 1:
        return 1

    list = [1]
    counter = 1
    num_in_row = n

    first_p_in_list = 0
    while 0 < n:
        first_p_in_list += n - 1
        n -= 1

    last_position = first_p_in_list + num_in_row - 1

    while counter < last_position * 2:
        counter += 2
        list.append(counter)
    result = 0
    while first_p_in_list < last_position + 1:
        result += list[first_p_in_list]
        first_p_in_list += 1
    print(result)
    return result

row_sum_odd_numbers(n)