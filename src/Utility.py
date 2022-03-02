def endsWith(endSeq: list[int], searchSeq: list[int]) -> bool:
    if len(endSeq) > len(searchSeq):
        return False

    return endSeq == searchSeq[-len(endSeq):]

def mean(l: list) -> float:
    return sum(l) / len(l)