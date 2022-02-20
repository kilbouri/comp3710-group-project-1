def endsWith(endSeq: list[int], searchSeq: list[int]) -> bool:
    if len(endSeq) > len(searchSeq):
        return False

    return endSeq == searchSeq[-len(endSeq):]
