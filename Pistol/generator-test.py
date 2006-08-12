def fib():
    a,b = 0,1
    while 1:
        yield b
        a,b = b,a+b

def main():
    f = fib()
    print f
    for i in range(20): print f.next()
    print [f for i in range(20)]
    return

if __name__ == '__main__': main()

