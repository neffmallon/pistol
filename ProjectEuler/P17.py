
words = {
    0: "",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety",
    100: "onehundred",
    200: "twohundred",
    300: "threehundred",
    400: "fourhundred",
    500: "fivehundred",
    600: "sixhundred",
    700: "sevenhundred",
    800: "eighthundred",
    900: "ninehundred",
    1000: "onethousand"
    }

def inwords(n):
    if n <= 20:
        nl = words[n]
    elif 20 <= n < 30:
        nl = words[20] + inwords(n-20)
    elif 30 <= n < 40:
        nl = words[30] + inwords(n-30)
    elif 40 <= n < 50:
        nl = words[40] + inwords(n-40)
    elif 50 <= n < 60:
        nl = words[50] + inwords(n-50)
    elif 60 <= n < 70:
        nl = words[60] + inwords(n-60)
    elif 70 <= n < 80:
        nl = words[70] + inwords(n-70)
    elif 80 <= n < 90:
        nl = words[80] + inwords(n-80)
    elif 90 <= n < 100:
        nl = words[90] + inwords(n-90)
    elif n == 100:
        nl = words[100]
    elif 100 < n < 200:
        nl = words[100] + 'and' + inwords(n-100)
    elif n == 200:
        nl = words[200]
    elif 200 < n < 300:
        nl = words[200] + 'and' + inwords(n-200)
    elif n == 300:
        nl = words[300]
    elif 300 < n < 400:
        nl = words[300] + 'and' + inwords(n-300)
    elif n == 400:
        nl = words[400]
    elif 400 < n < 500:
        nl = words[400] + 'and' + inwords(n-400)
    elif n == 500:
        nl = words[500]
    elif 500 < n < 600:
        nl = words[500] + 'and' + inwords(n-500)
    elif n == 600:
        nl = words[600]
    elif 600 < n < 700:
        nl = words[600] + 'and' + inwords(n-600)
    elif n == 700:
        nl = words[700]
    elif 700 < n < 800:
        nl = words[700] + 'and' + inwords(n-700)
    elif n == 800:
        nl = words[800]
    elif 800 < n < 900:
        nl = words[800] + 'and' + inwords(n-800)
    elif n == 900:
        nl = words[900]
    elif 900 < n < 1000:
        nl = words[900] + 'and' + inwords(n-900)
    elif n == 1000:
        nl = words[1000]
    return nl

def digsum(n):
    ints = range(1,n+1)
    lets = [inwords(i) for i in ints]
    print lets
    ns = [len(l) for l in lets]
    print sum(ns)

def randtest(n):
    from random import randrange
    for i in range(n):
        ir = randrange(1,1001)
        print ir,inwords(ir)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    #print inwords(342),len(inwords(342))
    #print inwords(115),len(inwords(115))
    #randtest(10)
    digsum(1000)
