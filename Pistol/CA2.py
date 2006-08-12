import Image
import ImageOps
import random

def step(a, rule, k=2, r=1):
    nbrs = [a[c:] + a[:c] for c in range(-r, r+1, 1)]
    l = []
    for t in apply(zip, nbrs):
        result = 0
        for i in t:
            result = (result * k) + i
        l.append(result)
    return [((rule / (k ** v)) % k) for v in l]

def basicRun(rule, steps, stepper, seed=[1], k=2, r=1):
    seed = ([0] * steps) + seed + ([0] * steps)
    result = seed[:]
    for i in range(steps):
        seed = stepper(seed, rule, k=k, r=r)
        result += seed[:]
    return result, (len(seed), steps + 1)

def showResult(result, dims, k=2):
    i = Image.new("L", dims)
    i.putdata(result, (255 / (k - 1)))
    i = i.crop(i.getbbox())
    i = ImageOps.invert(i)
    i.load()
    #i.show()
    i.save("bs.png","PNG")

def runTest():
    lines = 400
    result, dims = basicRun(110, lines, step)
    showResult(result, dims)

if __name__ == "__main__": runTest()
