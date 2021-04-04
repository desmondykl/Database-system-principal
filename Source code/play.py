# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 18:34:19 2020

@author: desmo
"""
import json
import psycopg2
import itertools


        
lst3 = list(itertools.product([False, True], repeat=3))
lst3 = lst3[1:-1]
lst2 = list(itertools.product([False, True], repeat=2))
lst2 = lst2[1:-1]
lst1 = list(itertools.product([False, True], repeat=1))

query = " EXPLAIN (FORMAT JSON) select l_orderkey, sum(l_extendedprice * (1 - l_discount)) as revenue, o_orderdate,o_shippriority from customer, orders, lineitem where c_mktsegment = 'BUILDING' and c_custkey = o_custkey and l_orderkey = o_orderkey group by l_orderkey, o_orderdate, o_shippriority order by revenue desc, o_orderdate "
s1 = [ "=false;" , "=true;"]

settings1 = []
settings1.append("set enable_hashjoin ")
settings1.append("set enable_mergejoin ")
settings1.append("set enable_nestloop ")

settings2 = []
settings2.append("set enable_indexscan ")
settings2.append("set enable_seqscan ")

settings3 = []
settings3.append("set enable_sort ")


configList = []
for slist3 in lst3:
    configQuery = ""
    for i in range(len(slist3)):
        if(not slist3[i]):
            configQuery = configQuery +  str(settings1[i]) + " = false; "
    configList.append(configQuery)
        
configList2 = []   
for slist2 in lst2:
    configQuery = ""
    for i in range(len(slist2)):
        if(not slist2[i]):
            configQuery = configQuery +  str(settings2[i]) + " = false; " 
    for c in configList:  
        configList2.append(c+configQuery)     

configList3 = []   
configList4 = ["set enable_sort  = false"]
for slist1 in lst1:
    configQuery = ""
    for i in range(len(slist1)):
        if(not slist1[i]):
            configQuery = configQuery +  str(settings3[i]) + " = false; " 
    for c in configList:  
        configList3.append(c+configQuery)  

configList5 = configList4 +  configList3 +  configList2 +  configList
configList6 = [] 
for i in configList5: 
    if i not in configList6: 
        configList6.append(i) 
configList6.insert(0,"")
planList = []
for config in configList6:
    try:
        connection = psycopg2.connect(user = "postgres",
                                      password = "password",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "TPC-H")
        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        # print ( connection.get_dsn_parameters(),"\n")
        # Print PostgreSQL version
        newQuery = str(config) + str(query)
        cursor.execute(newQuery)
        plan = cursor.fetchall() 
        result = []
        for row in plan:
            result.append(row[0])
        json_output = json.dumps(result[0][0])
        jsonObject = json.loads(json_output)
        planList.append(jsonObject)
        
    except (Exception, psycopg2.Error) as error :
               print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            
            
            
def traverse(node):
    for item in node:
        if 'Parent Relationship' in item:
            del item['Parent Relationship']   
        if 'Parallel Aware' in item:
            del item['Parallel Aware']   
        if 'Index Name' in item:
            del item['Index Name'] 
        if 'Alias' in item:
            del item['Alias'] 
        if 'Scan Direction' in item:
            del item['Scan Direction'] 
        if 'Plan Width' in item:
            del item['Plan Width'] 
        if 'Index Cond' in item:
            del item['Index Cond'] 
        if 'Strategy' in item:
            del item['Strategy']  
        if 'Group Key' in item:
            del item['Group Key']     
        if 'Partial Mode' in item:
            del item['Partial Mode']  
        if 'Inner Unique' in item:
            del item['Inner Unique']  
        if 'Join Type' in item:
            del item['Join Type']  
        if 'Presorted Key' in item:
            del item['Presorted Key']  
        if 'Sort Key' in item:
            del item['Sort Key']     
        if 'Total Cost' in item:
            del item['Total Cost']
        if 'Startup Cost' in item:
            del item['Startup Cost']
        if 'Workers Planned' in item:
            del item['Workers Planned']
        if 'Plan Rows' in item:
            del item['Plan Rows']
        if 'Filter' in item:
            del item['Filter']
            
        if "Plans" in item:
            traverse(item["Plans"])
    

def removeroot(item):
    if 'Parent Relationship' in item:
        del item['Parent Relationship']   
    if 'Parallel Aware' in item:
        del item['Parallel Aware']   
    if 'Index Name' in item:
        del item['Index Name'] 
    if 'Alias' in item:
        del item['Alias'] 
    if 'Scan Direction' in item:
        del item['Scan Direction'] 
    if 'Plan Width' in item:
        del item['Plan Width'] 
    if 'Index Cond' in item:
        del item['Index Cond'] 
    if 'Strategy' in item:
        del item['Strategy']  
    if 'Group Key' in item:
        del item['Group Key']     
    if 'Partial Mode' in item:
        del item['Partial Mode']  
    if 'Inner Unique' in item:
        del item['Inner Unique']  
    if 'Join Type' in item:
        del item['Join Type']  
    if 'Presorted Key' in item:
        del item['Presorted Key']  
    if 'Sort Key' in item:
        del item['Sort Key']     
    # if 'Total Cost' in item:
    #     del item['Total Cost']
    if 'Startup Cost' in item:
        del item['Startup Cost']
    if 'Workers Planned' in item:
        del item['Workers Planned']
    if 'Plan Rows' in item:
        del item['Plan Rows']
    if 'Filter' in item:
        del item['Filter']

originalplanList = planList.copy()
        
for pl in planList:         
    traverse(pl["Plan"]["Plans"])
    removeroot(pl["Plan"])

uplanList = []
upIndex = []
index = 0
for x in planList:
    if x not in uplanList:
        uplanList.append(x)
        upIndex.append(index)
    index += 1

