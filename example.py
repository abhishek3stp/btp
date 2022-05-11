from MaxMatching import MaxMatching


def printPair(MATE):
    for i in range(1, len(MATE)):
        if type(MATE[i]) == str:
            MATE[i] = int(MATE[i])
        
        elif MATE[i] != 0 and MATE[MATE[i]] == i:
            MATE[MATE[i]] = str(MATE[MATE[i]])
            print(i, MATE[i])


if __name__ == "__main__":
    v = int(input())
    e = int(input())
    maxMatching = MaxMatching(v)
    
    for _ in range(e):
        [n1, n2] = list(map(int, input().split()))
        maxMatching.addEdge(n1, n2)
    
    maxMatching.E()

    print("Maximum matching:")
    print(maxMatching.getMatchingSize()//2)

    print("Following are the matched edges:")
    printPair(maxMatching.MATE)
