from copy import deepcopy
from collections import defaultdict
from collections import OrderedDict
from operator import itemgetter
import os,sys,re
import pickle
from nltk.tokenize import *
from processing import grouping,remove_empty
result=open('total_result.txt','w')
neg_words =["bad", "issues", "wouldn't", "disappointing", "disappointed", "sick", "doesn't last", "except", "poor"]
def misc_calculate(misc):
    misc_score=defaultdict(int)
    misc_sent=defaultdict(list)
    for key in misc:
        for i in results[key]:
            for feature in features:
                reviews[feature]['pos']=list(set(reviews[feature]['pos']))
                reviews[feature]['neg']=list(set(reviews[feature]['neg']))
                feature_=' '.join(feature)
                if(i==feature_):
                    misc_score+=len(reviews[feature]['pos'])
                    for i in reviews[feature]['pos']:
                        misc_sent[key].append(review_text_tokenized[i[0]][i[1]])
                    misc_score-=len(reviews[feature]['neg'])
                    for i in reviews[feature]['neg']:
                        misc_sent[key].append(review_text_tokenized[i[0]][i[1]])
    return misc_score,misc_sent
def generate_feature_sentiments(feature_details,review_text_tokenized):
    reviews = {}
    features = []
    for key in feature_details: 
        features.append(key)
        pos_reviews = []
        neg_reviews = []
        # print key,":"
        reviews[key] = {}
        reviews[key]['pos'] = []
        reviews[key]['neg'] = []
        for i in feature_details[key]:
            neg = False
            for j in neg_words:
                if j in review_text_tokenized[i[0]][i[1]].lower():
                    neg = True
                    break
            if not neg:
                if i[2] > 0:
                    #print "Positive : ",review_text_tokenized[i[0]][i[1]]," -- ", i[3]
                    pos_reviews.append((i[0],i[1],i[2],i[3]))
                elif i[2] < 0:
                    #print "Negative : ",review_text_tokenized[i[0]][i[1]]," -- ",i[3]
                    neg_reviews.append((i[0],i[1],i[2],i[3]))
            else:
                if i[2] > 0:
                    #print "Negative : ",review_text_tokenized[i[0]][i[1]]," -- ",i[3]
                    neg_reviews.append((i[0],i[1],i[2],i[3]))
                elif i[2] < 0:
                    #print "Positive : ",review_text_tokenized[i[0]][i[1]]," -- ", i[3]
                    pos_reviews.append((i[0],i[1],i[2],i[3]))
               # print "Positive Reviews:""
        reviews[key]['pos'] = pos_reviews
        reviews[key]['neg'] = neg_reviews
    return features,reviews

if __name__ == "__main__":
    product = "Cell_Phones"
    them = os.listdir('Cell_Phones')
    asins = [file.strip('.json') for file in them]
    for asin in asins :
        review_text = open(product+'/'+asin+'.json','r').read()
        review_text=review_text.replace('-','.')
        review_text=review_text.replace('*','.')
        review_text=re.sub('\.+','.',review_text)
        review_text=re.sub('[^a-zA-Z0-9.\\s]+',' ',review_text)
        review_text=re.sub(r'([a-z]{2,})\1+', r'\1', review_text)
        review_text = re.sub('([.,;!?])\s*(\w)',r'\1 \2',review_text)
        review_text_copy = review_text
        reviews = review_text_copy.split('\n')
        reviews = [i for i in reviews if len(i) > 1]
        review_text_tokenized = [sent_tokenize(review) for review in reviews]
     
        # print [len(i) for i in reviews]
        feature_details = pickle.load(open('Features/'+asin+'_features','r'))
        features,reviews = generate_feature_sentiments(feature_details,review_text_tokenized)
        f = open('Reviews_Analysed/'+asin+'_Reviews_Analysed','w')
        x = ''
        fea_pos=defaultdict(int)
        fea_pos_sent=defaultdict(list)
        fea_neg=defaultdict(int)
        fea_neg_sent=defaultdict(list)
        results,misc=grouping(asin)
        rem_features=features
        for key in results:
            for i in results[key]:
                for feature in features:
                    reviews[feature]['pos']=list(set(reviews[feature]['pos']))
                    reviews[feature]['neg']=list(set(reviews[feature]['neg']))
                    feature_=' '.join(feature)
                    if(i==feature_):
                        rem_features.remove(feature)
                        fea_pos[key]+=len(reviews[feature]['pos'])
                        for i in reviews[feature]['pos']:
                            fea_pos_sent[key].append(review_text_tokenized[i[0]][i[1]])
                        fea_neg[key]-=len(reviews[feature]['neg'])
                        for i in reviews[feature]['neg']:
                            fea_neg_sent[key].append(review_text_tokenized[i[0]][i[1]])
        rem=defaultdict(int)
        rem_sent=defaultdict(list)
        for feature in rem_features:
                    feature_=' '.join(feature)
                    reviews[feature]['pos']=list(set(reviews[feature]['pos']))
                    rem[feature_]+=len(reviews[feature]['pos'])
                    for i in reviews[feature]['pos']:
                        rem_sent[feature_].append(review_text_tokenized[i[0]][i[1]])
                    reviews[feature]['neg']=list(set(reviews[feature]['neg']))
                    rem[feature_]-=len(reviews[feature]['neg'])
                    for i in reviews[feature]['neg']:
                        rem_sent[feature_].append(review_text_tokenized[i[0]][i[1]])
        rem={key:rem[key] for key in rem if rem[key]!=0}
        #print fea_pos.items()
        #print fea_pos_sent.items()
        
        rename_pos={'mobile':'good phone','battery':'good battery life','charge':'great charge','charging':'good charging', 'camera': 'good camera','display':'good display', 'performance':'good performance','speakers':'good speakers', 'assistant': 'helpful assistant'}
        rename_neg={'mobile':'bad phpone','battery':'bad battery','charge':'bad battery','charging':'bad charger','camera': 'bad camera', 'display': 'bad display', 'performance': 'bad performance','speakers':'bad speakers','assistant':'useless assistant'}
        #print fea_neg_sent.items()
        for i in rename_neg:
            if(fea_neg.has_key(i)):
                if(fea_neg[i]<0):
                    fea_neg[rename_neg[i]]=fea_neg.pop(i)
                    fea_neg_sent[rename_neg[i]]=fea_neg_sent.pop(i)
                else:
                    del fea_neg[i]
        for i in rename_pos:
            if(fea_pos.has_key(i)):
                if(fea_pos[i]>0):
                    fea_pos[rename_pos[i]]=fea_pos.pop(i)
                    fea_pos_sent[rename_pos[i]]=fea_pos_sent.pop(i)
                else:
                    del fea_pos[i]
        def printing(score,sent,fea_pos):
            score2=deepcopy(score)
            # print score2
            for i in score2:
                score2[i]=abs(score2[i])
            score2=OrderedDict(sorted(score2.items(),key=itemgetter(1),reverse=True))
            scorekeys=score2.keys()
            for i in scorekeys:
                f.write('\n--------------------------------------------------------\n')
                if(i in fea_pos):
                    got=[j for m in i.split()[1:] for j in fea_neg if m in j]
                    for k in got:
                        if(k in scorekeys):
                            f.write(k)
                            f.write('  ')
                            f.write(str(score[k]))
                            result.write(asin)
                            if (score[k] > 0):
                                result.write(' +')
                            else:
                                result.write(' -')
                            result.write(k)
                            result.write(',(%d)\n'%(score[k]))
                            sent[k]=list(set(sent[k]))
                            for j in sent[k]:
                                f.write('\n')
                                f.write(j)
                            scorekeys.remove(k)
                f.write(i)
                f.write('  ')
                f.write(str(score[i]))
                result.write(asin)
                if (score[i] > 0):
                    result.write(' +')
                else:
                    result.write(' -')
                result.write(i)
                result.write(',(%d)\n'%(score[i]))
                sent[i]=list(set(sent[i]))
                for j in sent[i]:
                    f.write('\n')
                    f.write(j)
        '''printing(fea_pos, fea_pos_sent)
        printing(fea_neg, fea_neg_sent)
        if(len(misc_score)!=0):printing(misc_score, misc_sent)
        printing(rem, rem_sent,1)'''
        misc_score,misc_sent=misc_calculate(misc)
        Total_scores={};Total_sents={}
        if(len(misc_score)!=0):
            Total_scores.update(misc_score)
            Total_sents.update(misc_sent)
        Total_scores.update(fea_pos);Total_scores.update(fea_neg);Total_scores.update(rem);
        Total_sents.update(fea_neg_sent);Total_sents.update(fea_pos_sent);Total_sents.update(rem_sent);
        
        printing(Total_scores,Total_sents,fea_pos)
        f.close()
    result.close()