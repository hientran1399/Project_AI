def read_file():
    file = open('input.txt', 'r')
    a = list(file)
    global res, lhs, domains, carry, n
    res = a[0].rstrip('\n').split('=')[1][::-1]
    lhs = a[0].rstrip('\n').split('=')[0][::-1].split('+')

    n = max([len(each) for each in lhs])
    for index in range(len(lhs)):
        lhs[index] = lhs[index] + "?"*(n-len(lhs[index]))

    domains = {}
    domains = init_domain(res, domains)
    for each_word in lhs:
        domains = init_domain(each_word, domains)
    carry = [-1]*(n+1)
    carry[0] = 0

    # non-zero leading
    domains[lhs[0][len(lhs[0])-1]][0] = 0
    domains[lhs[1][len(lhs[1])-1]][0] = 0
    domains[res[len(res)-1]][0] = 0


def init_domain(word, domains):
    for letter in word:
        domains[letter] = [1]*10
    return domains


def print_domain_carry():
    for key, value in domains.items():
        print(key, ': ', end='')
        for [index, item] in enumerate(value):
            if item == 1:
                print(index, ' ', end='')
        print()
    print('carry: ', carry)


def append_final(letter, num):
    global status, is_stop
    if letter in final and final[letter] == num:
        return
    if (letter in final) and (final[letter] != num):
        status = 'NO SOLUTION'
        is_stop = True
        return
    if (domains[letter][num] == 0):
        status = 'NO SOLUTION'
        is_stop = True
        return
    for key, value in final.items():
        if value == num:
            status = 'NO SOLUTION'
            is_stop = True
            return
    # append to final
    final[letter] = num
    for key, value in domains.items():
        domains[key][num] = 0
    tmp = [0]*10
    tmp[num] = 1
    domains[letter] = tmp
    is_stop = False


def check_unique():
    for key, value in domains.items():
        if sum(value) == 1:
            number = value.index(1)
            if (key not in final or final[key] != number):
                append_final(key, number)


def eliminate_greater(letter, num):
    global is_stop
    tmp = domains[letter]
    for index in range(10):
        if (index > num and tmp[index] != 0):
            tmp[index] = 0
            is_stop = False
    domains[letter] = tmp
    check_unique()


def eliminate_less(letter, num):
    global is_stop
    tmp = domains[letter]
    for index in range(10):
        if (index < num and tmp[index] != 0):
            tmp[index] = 0
            is_stop = False
    domains[letter] = tmp
    check_unique()


def eliminate_odd_even(letter, type):
    global is_stop
    tmp = domains[letter]
    t = 0
    if type == 'odd':
        t = 1
    for index in range(10):
        if (index % 2 == t and tmp[index] != 0):
            tmp[index] = 0
            is_stop = False
    domains[letter] = tmp
    check_unique()


def find_max(letter):
    for index in range(9, 0, -1):
        if domains[letter][index] == 1:
            return index
    return -1


def find_min(letter):
    for index in range(9):
        if domains[letter][index] == 1:
            return index
    return -1


def update_domain(letter, list):
    for i in range(10):
        if domains[letter][i] == 1 and i not in list:
            domains[letter][i] = 0


def rule_1():
    max_length = max([len(each) for each in lhs])
    if max_length < len(res):
        append_final(res[len(res)-1], 1)
        carry[len(res)-1] = 1
    if max_length == len(res):
        carry[len(carry)-1] = 0


def rule_3b(i, x, y, z):
    max_x = find_max(x)
    max_y = find_max(y)
    m = min(max_x, max_y)
    eliminate_greater(z, m)


def rule_5a(i, x, y, z):
    carry[i] = 1
    carry[i+1] = 0
    if (z not in in_distance):
        in_distance.append(z)
    if (y in final and final[y] == 0):
        distance[ord(x)-65][ord(z)-65] = 1
        distance[ord(z)-65][ord(x)-65] = -1
        if (x not in in_distance):
            in_distance.append(x)
    if (x in final and final[x] == 0):
        distance[ord(y)-65][ord(z)-65] = 1
        distance[ord(z)-65][ord(y)-65] = -1
        if (y not in in_distance):
            in_distance.append(y)


def rule_6b(i, x, y, z):
    if x in final:
        append_final(y, 10 + final[z] - final[x] - carry[i])
    if y in final:
        append_final(x, 10 + final[z] - final[y] - carry[i])


def rule_8(i, x, y, z):
    for a in range(26):
        for b in range(26):
            if distance[a][b] > 0:
                letter_A = chr(a+65)
                letter_B = chr(b+65)
                k = distance[a][b]
                max_b = find_max(letter_B)
                min_a = find_min(letter_A)
                eliminate_greater(letter_A, max_b-k)
                eliminate_less(letter_B, min_a+k)


def rule_7a(i, x, y, z):
    if distance[ord(z)-65][ord(x)-65] != 0 and carry[i+1] == 1:
        k = 10 - distance[ord(z)-65][ord(x)-65]
        # Rule 7a2
        if carry[i] > -1:
            append_final(y, k - carry[i])
        # Rule 7a1
        else:
            update_domain(y, [k, k-1])
            if (sum(domains[y]) == 1):
                if domains[y][k-1] == 1:
                    carry[i] = 1
                else:
                    carry[i] = 0
    if distance[ord(z)-65][ord(y)-65] != 0 and carry[i+1] == 1:
        k = 10 - distance[ord(z)-65][ord(y)-65]
        if carry[i] > -1:
            append_final(x, k - carry[i])
        else:
            update_domain(x, [k, k-1])
            if (sum(domains[x]) == 1):
                if domains[x][k-1] == 1:
                    carry[i] = 1
                else:
                    carry[i] = 0


def rule_2a(i, x, y, z):
    min_x = find_min(x)
    min_y = find_min(y)
    eliminate_less(z, min_x+min_y+carry[i])


def rule_2b(i, x, y, z):
    min_x = find_min(x)
    min_y = find_min(y)
    eliminate_less(z, min_x+min_y)


def rule_3a(i, x, y, z):
    k = 10 + find_min(z)
    max_y = find_max(y)
    max_x = find_max(x)
    t = k - max_y
    if max_y*2 == k:
        t += 1
    eliminate_less(x, t)
    t = k - max_x
    if max_x*2 == k:
        t += 1
    eliminate_less(y, t)


def rule_9a(i, x, y, z):
    if carry[i] == 0:
        domains[x][0] = 0
        eliminate_odd_even(z, 'odd')
    elif carry[i] == 1:
        eliminate_odd_even(z, 'even')

    if carry[i+1] == 0:
        eliminate_greater(x, 4)
    if carry[i+1] == 1:
        eliminate_less(x, 5)


def rule_9b(i, x, y, z):
    tmp = domains[z]
    list = []
    for index in range(10):
        if tmp[index] == 1:
            list.append((index-carry[i])/2)
            list.append((index-carry[i]+10)/2)
    update_domain(x, list)
    # tmp = domains[x]
    # list = []
    # for index in range(10):
    #     if tmp[index] == 1:
    #         list.append((index*2) % 10)
    # update_domain(z, list)


def rule_9c(i, x, y, z):
    tmp = domains[x]
    list = []
    if carry[i] == -1:
        for index in range(10):
            if tmp[index] == 1:
                list.append(2*index)
                list.append(2*index+1)
    else:
        for index in range(10):
            if tmp[index] == 1:
                list.append(2*index+carry[i])

    update_domain(z, list)


def main():
    global is_stop, status
    is_stop = False
    rule_1()
    count = 0

    while (not is_stop):
        count += 1
        is_stop = True
        status = ''
        for i in range(n-1, -1, -1):
            x = lhs[0][i]
            y = lhs[1][i]
            z = res[i]
            if x != z and y != z:
                if (carry[i+1] == 0 and carry[i] > -1):
                    rule_2a(i, x, y, z)

                if (carry[i+1] == 0 and carry[i] == -1):
                    rule_2b(i, x, y, z)

                if carry[i+1] == 1 and carry[i] == 0 and x != y:
                    rule_3a(i, x, y, z)

                if carry[i+1] == 1 and carry[i] == - 1 and x != y:
                    rule_3b(i, x, y, z)

            if x == y and x != z:
                rule_9a(i, x, y, z)
                if carry[i+1] == -1 and carry[i] != -1:
                    rule_9b(i, x, y, z)
                if carry[i+1] == 0:
                    rule_9c(i, x, y, z)

            if (y in final and final[y] == 0 and x != y and x != z) or (x in final and final[x] == 0 and x != y and y != z):
                rule_5a(i, x, y, z)

            if (x not in final or y not in final or z not in final):
                # Rule 6c
                if (carry[i] > -1 and x in final and y in final):
                    append_final(z, (final[x] + final[y] + carry[i]) % 10)

                # Rule 6b
                if (carry[i+1] > -1 and carry[i] > -1 and z in final and (x in final or y in final)):
                    rule_6b(i, x, y, z)

            # coi lai cai dieu kien sum tai vi vua co -1. vuawf co 1
            if x in in_distance or y in in_distance or z in in_distance:
                rule_7a(i, x, y, z)

        if len(in_distance) > 0:
            rule_8(i, x, y, z)
    if status == 'NO SOLUTION':
        print(status)
    else:
        print_domain_carry()
    print('loop: ', count, ' times.')


final = {}
distance = [[0 for i in range(26)] for j in range(26)]
in_distance = []
read_file()
main()
