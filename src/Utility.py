def endsWith(endSeq: list[int], searchSeq: list[int]) -> bool:
    if len(endSeq) > len(searchSeq):
        return False

    return endSeq == searchSeq[-len(endSeq):]

def mean(l: list) -> float:
    return sum(l) / len(l)


def allsame(lst):
    # Returns True if all elements in a list are the same
    return all(x == lst[0] for x in lst)