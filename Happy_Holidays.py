#Write a function that accepts a sequence of Reindeer names, and returns a sequence with the Reindeer names sorted by their last names.
# Notes:
# It's guaranteed that each string is composed of two words
# In case of two identical last names, keep the original

reindeer_names = [
  "Dasher Tonoyan",
  "Dancer Moore",
  "Prancer Chua",
  "Vixen Hall",
  "Comet Karavani",
  "Cupid Foroutan",
  "Donder Jonker",
  "Blitzen Claus"
]

def sort_reindeer(reindeer_names):
    if reindeer_names == []:
        return []
    position = []
    dic = {}
    new_list = []
    for i in reindeer_names:
        position = i.split(" ")
        term = "surename"
        dic[term] = position[0]
        term1 = "lastname"
        dic[term1] = position[1]
        new_list.append(dic.copy())

    def my_Func(lastname1):
        return lastname1["lastname"]

    new_list.sort(key=my_Func)
    new_list1 = []
    for i in new_list:
        new_list1.append(i["surename"] + " " + i["lastname"])

    return new_list1

sort_reindeer(reindeer_names)
print (sort_reindeer(reindeer_names))