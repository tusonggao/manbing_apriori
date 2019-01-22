from votesmart import votesmart


def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset, C1)

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if can not in ssCnt:
                    ssCnt[can]=1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData

def aprioriGen(Lk, k): #creates Ck
    retList = []
    lenLk = len(Lk)
    for i in range(LenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1==L2:
                retList.append(Lk[i] | Lk[j])
    return retList

def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while(len(L[k-2])>0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


def generateRules(L, supportData, minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList



def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq]
        if conf >= minConf:
            print(freqSet-conseq,'-->',conseq,'conf:',conf)
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH



def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = aprioriGen(H, m + 1)
    Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
    if (len(Hmp1) > 1):
        rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)


#
# dataSet=loadDataSet()
# print('dataSet is', dataSet)
#
# C1=createC1(dataSet)
# print('C1 is', C1)
#
# D=map(set, dataSet)
# print('D is', D)
#
# L1, suppData0=scanD(D, C1, 0.5)
# print(L1)
#
# C1 = createC1(dataSet)
#
# L, suppData = apriori(dataSet)

votesmart.apikey = '49024thereoncewasamanfromnantucket94040'
bills = votesmart.votes.getBillsByStateRecent()

for bill in bills:
    print(bill.title,bill.billId)

bill = votesmart.votesmart.votes.getBill(11820)
print(bill.actions)

voteList = votesmart.votesmart.votes.getBillActionVotes(31670)
print(voteList[22])

for key in transDict.keys():
    print(transDict[key])


if __name__=='__name__':
    print('helo world!')
    prin('otput apriori fthemem')