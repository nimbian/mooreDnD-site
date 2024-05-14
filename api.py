from sqlhelper import *

def apiGetAll():
    out = getAllCollections()
    tmp = []
    for t in out:
        tmp += [list(t[:6]) + ['Yes' if t[6] else 'No',] + [t[7] if t[7] else 'Unlimited',] + list(t[8:])]
    return tmp

def apiGetCs(did,c):
    tmp = getCardsForUser(did,c)
    x = []
    for t in tmp:
        x += [t[:5]+ ('Yes' if t[5] else 'No',) + t[6:8] + t[-1:]]
    return x

def apiGetCards(did,s):
    if type(did) != str:
            return []
    s = s.replace('_',' ').replace('8',"'").replace('9','?')
    if s == 'Full Collection':
        tmp = getFullCollection(did)
        x = []
        for t in tmp:
            x += [t[:5]+ ('Yes' if t[5] else 'No',) + t[6:8] + t[-1:]]
        return x
    elif s == 'Monsters':
        return getAllMonsters(did)
    elif s == 'Items':
        return getAllItems(did)
    else:
        st = getCardsInSetByName(s)
        col = getFullCollection(did)
        tmp = {}
        for c in col:
            if not c[9] in tmp:
                tmp[c[9]] = []
            tmp[c[9]] += [[c]]
        out = []
        for ss in st:
            #out += [['', ss[1], 'Yes' if ss[0] in tmp.keys() else 'No', len(tmp.get(ss[0],[]))]]
            out += [{'name':ss[1], 'has': 'Yes' if ss[0] in tmp.keys() else 'No', 'count': len(tmp.get(ss[0],[])), 'cs': tmp.get(ss[0],[])}]
    return out
