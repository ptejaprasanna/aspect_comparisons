from collections import OrderedDict
def curate(asin):
    fi=open('FeatureList/'+asin+'_features','r')
    features=fi.readlines()
    feat=[]
    for i in features:
        i=i.strip()
        i=i.strip("(' ')")
        i=' '.join([i])
        i=i.replace('\'','')
        i=i.replace(',','')
        feat.append(i)
    return feat
def grouping(asin):
    features=curate(asin)
    print features
    #extra=['RAM','Siri','Water resistant','dollars','price','money','internal memory','external memory','processor','screen size','flash', 'assisstant']
    extra = []
    lis = ['mobile', 'battery', 'charge','charging','notch', 'bixby', 'camera', 'display', 'assistant', 'Siri','ip67','water resistant', 'interface','headphone jack','performace','processor']
    pre = {'mobile':['phone','product','handset','device','mobile', 'cellphone'],'battery':['battery','backup','charge']}
    
    for key in lis:
        synonyms=[]
        for i in features:
            if(pre.has_key(key)):
                value=[(i) for term in pre[key] if term.lower() in i.lower()]
            else:
                if term.lower() in i.lower():value=[i]
            if len(value):features.remove(value[0])
            synonyms.extend(value)
        if(pre.has_key(key)):
            final[key]=synonyms
        else:
            misc[key]=synonyms
    final=remove_empty(final)
    misc=remove_empty(misc)
    return final,misc
def remove_empty(final):
    final={key:final[key] for key in final if len(final[key])!=0}
    return final
def number(asin):
    reviews=open('no_of_reviews.txt','r')
    reviews.readlines()
