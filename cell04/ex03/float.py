A = input("Give me a number : ")
if '.' in A:
    if float(A).is_integer():
        print("This number is an integer.")
    else:
        print("This number is a decimal.")
else:
    print("This number is an integer.")