def mone(non):
    a = 0
    for i in  str(non):
            a += 1
    return a
print(mone("73654108430135874305"))

result = (x * x for x in range(1, 101) if x % 2 == 0)

print(sum(result))