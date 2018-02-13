def chunks(list_, n, length=None):
    if length is None:
        length = len(list_)
    """Yield successive n-sized chunks from l."""
    for i in range(0, length, n):
        yield list_[i:i + n]