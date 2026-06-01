# region str
my_string = 'hello my name is ruti ruti'


#
# def clean(str1):
#     for i in str1:
#         if not i.isalnum() or not i.isalpha():
#             str1 = str1.replace(i, '')
#     return str1
#
#
# print(clean(my_string))
#
#
# def pupular(str1):
#     count = 0
#     word = ""
#     arr = str1.split()
#     for i in arr:
#         if str1.count(i) > count:
#             count = str1.count(i)
#             word = i
#     return word
#
#
# print(pupular(my_string))

# endregion

def analyze_list(lst):
    sum = 0
    unique_list = set(lst)
    singel = unique_list
    for i in lst:
        sum += i
    avg = sum / len(lst)
    lst.sort()
    max = lst[0]
    min = lst[len(lst) - 1]
    dec = {"singed": singel, "avg": avg, "max:": max, "min:": min}
    return dec


list = [1, 2, 3, 4, 4]
print(analyze_list(list))


def filter_dict(d, threshold):
    list = []
    for i in d:
        if d[i] > threshold:
            list.append(i)
    return list


d = {"Rut": 45000, "Sari": 98000, "Erat": 12000, "Noa": 56000}
print(filter_dict(d, 20000))
