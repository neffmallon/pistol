def grep(fname,pat):
    if type(pat) == type(''): pat = re.compile(pat)
    result = None
    for line in open(fname):
        if pat.search(line): result = line
    return result
