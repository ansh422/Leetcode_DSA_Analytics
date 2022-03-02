'''
Made by: Ansh Gupta
Created on: 01/03/2022; 

'''

from plotly.subplots import make_subplots
import plotly.express as px
import plotly.offline as pof
import pandas as pd
import warnings
import requests
import subprocess
import json
import sys
import os

warnings.filterwarnings("ignore")

def extract_json(dict):
  user=dict['user']
  opName=dict['opName']
  Query=dict['Query']
  data={
  "operationName": opName,
  "variables": {"username":user},
  "query": Query
  }
  header={
      "Referer":f"https://leetcode.com/{user}",
      'Content-type':'application/json'
  
  }
  s=requests.session()
  s.get("https://leetcode.com/")
  header["x-csrftoken"] = s.cookies["csrftoken"]
  r = s.post("https://leetcode.com/graphql",json=data,headers=header)
  return json.loads(r.text)

def util(fig):
  traces=[]
  for trace in range(len(fig['data'])):
    traces.append(fig['data'][trace])
  return traces

def main_func(user):
  #user=input("Enter your Leetcode User Name: ")
  Query="""query skillStats($username: String!) {
    matchedUser(username: $username) {
      tagProblemCounts {
        advanced {
          tagName
          problemsSolved
        }
        intermediate {
          tagName
          problemsSolved
        }
        fundamental {
          tagName
          problemsSolved
        }
      }
    }
  }"""
  json_data1=extract_json({"user":user,"opName":"skillStats","Query":Query})
  try:
    df_data1 = json_data1['data']['matchedUser']['tagProblemCounts']['intermediate']
    df_data2=json_data1['data']['matchedUser']['tagProblemCounts']['fundamental']
    df_data3=json_data1['data']['matchedUser']['tagProblemCounts']['advanced']
    df_intermediate= pd.DataFrame(df_data1)
    df_fundamental= pd.DataFrame(df_data2)
    df_advanced= pd.DataFrame(df_data3)
  except:
    return ("<h1>The user does not exist!</h1>")
  
  frames=[df_fundamental,df_intermediate,df_advanced]
  res=pd.concat(frames,ignore_index=True)
  data_structures=['Array','Matrix','String','Stack','Queue','Linked List','Tree','Binary Tree','Hash Table','Graph','Trie','Union Find']
  algorithms=['Sorting','Two Pointers','Greedy','Binary Search','Depth-First Search','Breadth-First Search','Recursion','Sliding Window','Backtracking','Dynamic Programming','Divide and Conquer','Topological Sort','Shortest Path']

  if res.empty:
    return ("<h1>You have not attempted a single question!</h1>")
  
 # print("Data Received from Leetcode")
  data_structure_df=res.loc[res['tagName'].isin(data_structures)]
  data_structure_df=data_structure_df.reset_index(drop=True)
  data_df=data_structure_df.sort_values(by=['problemsSolved'])

  
  data_bar = px.bar(data_df, x="problemsSolved", y="tagName",orientation='h')
  radar_data = (px.line_polar(data_df, r='problemsSolved', theta='tagName', line_close=True)).update_traces(fill='toself')
  data_pie=(px.pie(data_structure_df,values='problemsSolved',names='tagName')).update_layout(showlegend=False)

  algorithm_df=res.loc[res['tagName'].isin(algorithms)]
  algorithm_df=algorithm_df.reset_index(drop=True)
  algo_df=algorithm_df.sort_values(by=['problemsSolved'])

  algo_bar = px.bar(algo_df, x="problemsSolved", y="tagName",orientation='h')
  algo_radar = (px.line_polar(algo_df, r='problemsSolved', theta='tagName', line_close=True)).update_traces(fill='toself')
  algo_pie=(px.pie(algorithm_df,values='problemsSolved',names='tagName')).update_layout(showlegend=False)


  data_bar_traces=util(data_bar)
  data_radar_traces=util(radar_data)
  data_pie_traces=util(data_pie)
  algo_bar_traces=util(algo_bar)
  algo_radar_traces=util(algo_radar)
  algo_pie_traces=util(algo_pie)

  data_fig = make_subplots(rows=2, cols=2,specs=[[{"type":"xy"},{"type":"domain"}],[{"type":"polar"},{"type":"domain"}]],subplot_titles=("Number of question done by Data Structure","% of questions done by Data Structures","","Radar Chart showing number of question by Data Structures"))
  for trace in data_bar_traces:
    data_fig.append_trace(trace,row=1,col=1)
  for trace in data_radar_traces:
    data_fig.append_trace(trace,row=2,col=1)
  for trace in data_pie_traces:
    data_fig.append_trace(trace,row=1,col=2)
  data_fig.update_layout(height=900,width=1200)
  data_graph=pof.plot(data_fig, include_plotlyjs=False, output_type='div')

  algo_fig = make_subplots(rows=2, cols=2,specs=[[{"type":"xy"},{"type":"domain"}],[{"type":"polar"},{"type":"domain"}]],subplot_titles=("Number of question done by Algorithm","% of questions done by Algorithm","","Radar Chart showing number of question by Algorithm"))
  for trace in algo_bar_traces:
    algo_fig.append_trace(trace,row=1,col=1)
  for trace in algo_radar_traces:
    algo_fig.append_trace(trace,row=2,col=1)
  for trace in algo_pie_traces:
    algo_fig.append_trace(trace,row=1,col=2)
  algo_fig.update_layout(height=900,width=1200)
  algo_graph=pof.plot(algo_fig, include_plotlyjs=False, output_type='div')
  #print("Charts created")

  html_report="<script src=\"https://cdn.plot.ly/plotly-latest.min.js\"></script>"
  #html_report+="<style>*{text-align: center;color: #99CCFF;}h1{text-decoration: underline;}footer{color: black;}</style>"
  html_report+="<h2>Data Structure </h2>"
  html_report+=data_graph
  html_report+="<h2>Algorithms</h2>"
  html_report+=algo_graph
  #html_report+="<hr><footer>&#169; Made by: <a href=\"https://anshgupta.tech\">Ansh Gupta.</a></footer>"

  return html_report

  

  #hs = open("leetcodereport.html", 'w+')
  #hs.write(html_report) 
  #hs.close()
  #print("Report formed")



  
  #url=os.path.join(os.getcwd(),'leetcodereport.html')
  #try:
  #  os.startfile(url)
  #except AttributeError:
  #  try:
  #    subprocess.call(['open',url])
  #  except:
  #    print("The report is saved here:")
  #    print(url)
#
'''
Made by: Ansh Gupta
Created on: 01/03/2022; 

'''