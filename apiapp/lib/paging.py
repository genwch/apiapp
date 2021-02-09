def data_paging(data, paging, page):
    rtn = data[paging*(page-1):paging*(page)]
    return rtn, int(len(data)/paging)+1
