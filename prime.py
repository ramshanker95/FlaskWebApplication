# number = int(input("Enter Number: "))
# counter = 0
# i = 0
# while True:
#     if i%3 == 0 or i%5==0 or i%7 == 0:
#         print(i)
#     i +=1
#     if counter == 6:
#         break
#     counter += 1

st = input("Enter String: ")
div = int(input("Number of Div: "))

if len(st)%div == 0:
    sub_s = len(st)/div
    for i in range(0, len(st), int(sub_s)):
        print(st[i:i + int(sub_s)], end=" ")
else:
    print("Invaild String")