while True:
    a = int(input("Enter a number : "))
    if a == a:
        for i in range(0, 10):
            print(f"{i} * {a} = {a * i}")
        break
    else:
        print("Error")