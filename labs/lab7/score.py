import sys

def readData():
    if len(sys.argv) != 4:
        print("Usage: python score.py (tag|lemma) goldfile sysfile")
        exit()

    if not sys.argv[1] in ["tag", "lemma"]:
        print("Unknown command line argument: " + sys.argv[1])

    try:
        gfile = open(sys.argv[2], encoding='iso-8859-1', errors='ignore')
        gtokens = gfile.readlines()
    except IOError:
        print("Couldn't read data from gold file")
        exit()

    try:
        sfile = open(sys.argv[3], encoding='iso-8859-1', errors='ignore')
        stokens = sfile.readlines()
    except IOError:
        print("Couldn't read data from sys file")
        exit()

    if len(gtokens) != len(stokens):
        print("Gold and sys files don't have the same number of lines")
        exit()

    return zip(gtokens, stokens)

def scoreTokens(pos, data):
    tokcount = 0
    errcount = 0
    tpcount = {}
    fpcount = {}
    fncount = {}

    for (g, s) in data:
        gs = g.strip().split("\t")
        ss = s.strip().split("\t")
        if gs[0] or ss[0]:  # At least one non-empty line
            if len(gs) <= pos:
                print("Not enough columns in gold file:")
                print(g)
                exit()
            if len(ss) <= pos:
                print("Not enough columns in sys file:")
                print(s)
                exit()
            if gs[0] != ss[0]:
                print("Different tokens: {0} ≠ {1}".format(gs[0], ss[0]))
                exit()
            tokcount += 1
            if gs[pos] != ss[pos]:
                errcount += 1
                if pos == 1:
                    if not gs[pos] in fncount:
                        fncount[gs[pos]] = 1
                    else:
                        fncount[gs[pos]] += 1
                    if not ss[pos] in fpcount:
                        fpcount[ss[pos]] = 1
                    else:
                        fpcount[ss[pos]] += 1
            elif pos == 1:
                if not gs[pos] in tpcount:
                    tpcount[gs[pos]] = 1
                else:
                    tpcount[gs[pos]] += 1
    if pos == 1:
        return [tokcount, errcount, tpcount, fpcount, fncount]
    else:
        return [tokcount, errcount]

def printResults(pos, scores):
    tokcount = scores[0]
    errcount = scores[1]
    corrcount = tokcount - errcount
    accuracy = corrcount / tokcount
    print("\nAccuracy: {0:.2f}% ({1}/{2})".format(accuracy * 100, corrcount, tokcount))

    if pos == 1:
        tpcount = scores[2]
        fpcount = scores[3]
        fncount = scores[4]
        print("\nTag\tCount\tPrec\tRec\n--------------------------------")
        for tag in sorted(tpcount):
            if tag in tpcount:
                tp = tpcount[tag]
            else:
                tp = 0
            if tag in fpcount:
                fp = fpcount[tag]
            else:
                fp = 0
            if tag in fncount:
                fn = fncount[tag]
            else:
                fn = 0
            print("{0}\t{1}\t{2:.2f}%\t{3:.2f}%".format(tag, tp + fn, 100 * tp / (fp + tp), 100 * tp / (fn + tp)))

    print()

# main
        
data = readData()

if sys.argv[1] == "lemma":
    pos = 2
else:
    pos = 1

scores = scoreTokens(pos, data)
printResults(pos, scores)


