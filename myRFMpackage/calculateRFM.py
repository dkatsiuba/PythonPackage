#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:58:56 2019

@author: katsiuba
"""

import pandas as pd

def calculateRFM(data, weight_recency=1, weight_frequency=1, weight_monetary=1):
     
    """
    Calculate a weighted RFM score
    @param data 
    @param
    @return
    @raise
    """
    
    # Ensure that the weights add up to one
    weight_recency2 = weight_recency/sum([weight_recency, weight_frequency, weight_monetary])
    weight_frequency2 = weight_frequency/sum([weight_recency, weight_frequency, weight_monetary])
    weight_monetary2 = weight_monetary/sum([weight_recency, weight_frequency, weight_monetary])
    
    # RFM measures
    max_Date=max(data["TransDate"])
    rfm=data.groupby("Customer", as_index=False).agg({"TransDate":"max",#recency = difference between latest transaction and "today"
                    "Quantity": "count", #frequency = number of transactions
                    "PurchAmount":"mean"}) #monetary = average amount spent per transaction
    #rename the colums
    rfm.rename(columns = {"TransDate":"Recency", "Quantity":"Frequency", "PurchAmount": "Monetary"}, inplace=True)
    #recency is defined as max.date - last purchase
    rfm["Recency"]=max_Date-rfm["Recency"]
    #make sure recency is numeric
    rfm["Recency"]=rfm["Recency"].dt.days

    # RFM scores
    rfm_scores = rfm.copy()

    #we need to add plus one otherwise bins=0-2
    #here we need to invert the scale
    rfm_scores['Recency'] = pd.qcut(rfm_scores['Recency']*-1,q=3,labels=False, duplicates='drop') + 1

    #here we need to use a rank function first because qcut cannot put the same value in different bins.
    rfm_scores['Frequency'] = pd.qcut(rfm_scores['Frequency'].rank(method='first'),q=3,labels=False, duplicates='raise') + 1

    rfm_scores['Monetary'] = pd.qcut(rfm_scores['Monetary'],q=3,labels=False, duplicates='drop') + 1

    # Overall RFM score
    rfm_scores["Finalscore"]=rfm["Frequency"]*weight_frequency2+rfm["Monetary"]*weight_monetary2+rfm["Recency"]*weight_recency2
    
    # RFM group
    rfm_scores["group"]=round(rfm_scores["Finalscore"])
    
    return rfm_scores