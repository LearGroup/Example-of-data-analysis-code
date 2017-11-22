# -*- coding:utf-8 -*-
import sys
from math import sqrt

critics={'Lisa Rose':
             {u"哈素海": 3.5, u"大召寺": 5.0,
              u"大青山野生动物园": 2.0, u"席力图召": 2.5,
              u"万部华严经塔": 3.5, u"乌兰夫纪念馆": 1.5,
              u"昭君墓": 4.0, u"内蒙古博物馆": 2.0,

              u"清水河老牛湾": 1.5,
              u"白石头沟生态旅游区": 3.5},
         'Gene Seymour':
             {u"哈素海": 4.0, u"大召寺": 3.0,
              u"大青山野生动物园": 2.0, u"席力图召": 3.5,
              u"万部华严经塔": 3.5, u"乌兰夫纪念馆": 3.5,
              u"昭君墓": 3.0, u"内蒙古博物馆": 2.0,
              u"清水河老牛湾": 4.5, u"白石头沟生态旅游区": 3.0},
         'Machael Phillips':
             {u"哈素海": 2.0, u"大召寺": 4.5,
              u"大青山野生动物园": 5.0, u"席力图召": 3.5,
              u"万部华严经塔": 2.5, u"乌兰夫纪念馆": 2.0,
              u"昭君墓": 4.0, u"内蒙古博物馆": 4.0,

              u"清水河老牛湾": 2.5,
              u"白石头沟生态旅游区": 3.5},
         'Mick LaSalle':
             {u"哈素海": 1.0, u"大召寺": 3.0,
              u"大青山野生动物园": 2.0, u"席力图召": 3.5,
              u"万部华严经塔": 2.0, u"乌兰夫纪念馆": 1.0,
              u"昭君墓": 5.0, u"内蒙古博物馆": 4.0,

              u"清水河老牛湾": 4.5,
              u"白石头沟生态旅游区": 2.0},
         'Claudia Puig':
             {u"哈素海": 1.5, u"大召寺": 4.0,
              u"大青山野生动物园": 3.0, u"席力图召": 4,
              u"万部华严经塔": 2.0,
              u"昭君墓": 3.0, u"内蒙古博物馆": 3.5,
              u"乌兰夫纪念馆": 3.0,
             u"清水河老牛湾": 4.5,
              u"白石头沟生态旅游区": 4.0},
         'Jack Matthews':
             {u"哈素海": 3.0, u"大召寺": 4.0,
               u"大青山野生动物园": 5.0,u"席力图召":3.0,
              u"万部华严经塔": 5.0, u"乌兰夫纪念馆": 3.0,
              u"昭君墓": 5.0, u"内蒙古博物馆": 3.0,
             u"乌兰夫纪念馆": 3.0,
              u"清水河老牛湾":1.5,u"昭君墓": 3.5,
              u"白石头沟生态旅游区": 3.0},
         '陈广平':
             { u"哈素海": 3.5, u"大召寺": 4.5,
              u"大青山野生动物园": 1.0},

         }
def sim_pearson(prefs,p1,p2):
    #得到双方收评价过过的列表
    si={}
    for item in prefs[p1]:
        if item in prefs[p2] :si[item]=1
    n=len(si)
    if n==0 :return 1

    #对所有偏好求和
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])
    #求平方和
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

    #求乘积之和
    pSum =sum([prefs[p1][it]*prefs[p2][it] for it in si])

    #计算皮尔逊评价值
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))

    if den==0:return 0
    r = round( num/den,5)
    return r


def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]
    #对列表进行排序 ，评价值最高在前
    scores.sort()
    scores.reverse()
    return scores[0:n]

# 利用所有他人评价值的加权平均，为某人提供建议
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        if other==person:continue
        sim=similarity(prefs,person,other)
        #忽略评价值为零或小于零的情况
        if sim<=0:continue
        for item in prefs[other]:
            #只对自己还未曾看过的影片进行评价
            if item not in prefs[person]  or prefs[person][item]==0:
                #相似度*评价值
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                simSums.setdefault(item,0)
                simSums[item]+=sim
    rankings=[(round(total/simSums[item],3),item) for item ,total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            result[item][person]=prefs[person][item]
    return result


def calculateSimilarItems(prefs,n=10):
    result={}
    #以物品为中心对偏好进行倒置
    itemPrefs=transformPrefs(prefs)
    c=0
    for item in itemPrefs:
        #针对大数据集更新状态变量
        c+=1
        if c%100==0:print "%d / %d"%(c,len(itemPrefs))
        # 寻找最为相近的物品
        scores=topMatches(itemPrefs,item,n=n,similarity=sim_pearson)
        result[item]=scores
    return result

def getRecommendedItems(prefs,itemMath,user):
    userRatings=prefs[user]
    scores={}
    totalSim={}

    #循环遍历由当前用户评分的物品
    for(item,rating) in userRatings.items():
        #循环遍历与当前物品相近的物品
        for(similarity,item2) in itemMath[item]:
            #如果该用户已对当前物品做过评价，则将其忽略
            if item2 in userRatings:continue
            #评价值与相似度的加权之和
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating
            #全部相似度之和
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity
    #将每个合计值除以加权和，求出平均值
    rankings=[(score/totalSim[item],item) for item,score in scores.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

if __name__=="__main__":
    #print topMatches(critics,'Toby',n=10)
    #print getRecommendations(critics,"Toby",similarity=sim_pearson)
    #print topMatches(transformPrefs(critics),'Superman Returnss',n=6)
   for item in getRecommendedItems(critics,calculateSimilarItems(critics),"陈广平"):
       print item[1],round(item[0],3)
