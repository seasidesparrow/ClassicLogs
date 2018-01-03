#!/usr/bin/env python

def create_or_append(k1,k2,dct):
    try:
        dct[k1]
    except KeyError:
        dct[k1]=[k2]
    else:
        dct[k1].append(k2)
    return

def select_multis(dct,n):
    out = [(k,dct[k]) for k in dct.keys() if len(dct[k]) > n]
    return out

def all_links_parser(filename):

    ads_all_links = filename

    bib_doikeyed = {}
    doi_bibkeyed = {}

    errors = ['Duplicate DOIs for bibcode:','Duplicate bibcodes for DOI:']

    with open(filename,'rU') as fl:
        for l in fl.readlines():
            (bibc,doi) = l.strip().split('\t')
            create_or_append(doi,bibc,bib_doikeyed)
            create_or_append(bibc,doi,doi_bibkeyed)
    
    out0 = [(errors[0],a,b) for (a,b) in select_multis(doi_bibkeyed,1)]
    out1 = [(errors[1],a,b) for (a,b) in select_multis(bib_doikeyed,1)]

#   do whatever you want with out0,1 here: return/print the tuple, or turn
#   it into a dictionary/json object

    for a,b,c in out0:
        print "%s\t%s\t%s"%(a,b,c)
    for a,b,c in out1:
        print "%s\t%s\t%s"%(a,b,c)

    return


def main():
    parse_all_links()


if __name__ == '__main__':
    main()
