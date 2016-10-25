import plotly
from plotly.graph_objs import Scatter, Layout, Data
from plotly.tools import FigureFactory as FF
from os import remove
from time import sleep

topSeven = ['Leicester', 'Arsenal', 'Tottenham', 'Man City', 'Man United', 'Chelsea', 'Southampton']
middleSix = ['West Ham', 'Stoke City', 'Everton', 'Swansea', 'Watford', 'West Brom']
bottomSix = ['Crystal Palace', 'Bournemouth', 'Sunderland', 'Middlesbrough', 'Hull', 'Burnley']

'''
top 7: draw home/away
middle 6: win home/draw away
bottom 6: win home/away
'''

fixtures = [
    ['Arsenal', 'A'],
    ['Burnley', 'A'],
    ['Tottenham', 'A'],
    ['Leicester', 'H'],
    ['Chelsea', 'A'],
    ['Hull', 'H'],
    ['Swansea', 'A'],
    ['Man United', 'H'],
    ['West Brom', 'H'],
    ['Crystal Palace', 'A'],
    ['Watford', 'H'],
    ['Southampton', 'A'],
    ['Sunderland', 'H'],
    ['Bournemouth', 'A'],
    ['West Ham', 'H'],
    ['Middlesbrough', 'A'],
    ['Everton', 'A'],
    ['Stoke', 'H'],
    ['Man City', 'H'],
    ['Sunderland', 'A'],
    ['Man United', 'A'],
    ['Swansea', 'H'],
    ['Chelsea', 'H'],
    ['Hull', 'A'],
    ['Tottenham', 'H'],
    ['Leicester', 'A'],
    ['Arsenal', 'H'],
    ['Burnley', 'H'],
    ['Man City', 'A'],
    ['Everton', 'H'],
    ['Bournemouth', 'H'],
    ['Stoke', 'A'],
    ['West Brom', 'A'],
    ['Crystal Palace', 'H'],
    ['Watford', 'A'],
    ['Southampton', 'H'],
    ['West Ham', 'A'],
    ['Middlesbrough', 'H']
]

results = "WLDWWWWDW"

alternativeTable = []

runningTarget=0
runningActual=0

for match in fixtures:
    opponent = match[0]
    homeaway = match[1]
    if opponent in topSeven:
        targetPoints=1
    elif opponent in bottomSix:
        targetPoints=3
    elif homeaway=="H":
        targetPoints=3
    else:
        targetPoints=1

    runningTarget+=targetPoints
    alternativeTable.append([opponent,homeaway,targetPoints,'',runningTarget,''])


for i in range(len(results)):
    res = results[i]
    if res=="W":
        r=3
    elif res=="D":
        r=1
    else:
        r=0

    alternativeTable[i][3]=r

    runningActual+=r
    alternativeTable[i][5]=runningActual

## TABLE ##

data_matrix = [['Gameweek','Opponent','H/A','Target Points','Actual Points','Running Target','Running Actual','Difference']]

gw=0
totalDifferences=[]
for match in alternativeTable:
    gw+=1
    opponent = match[0]
    homeaway = "Home" if match[1]=="H" else "Away"
    targetPoints = match[2]
    actualPoints = match[3]
    runningTarget = match[4]
    runningActual = match[5]
    if len(str(runningTarget))>0 and len(str(runningActual))>0:
        difference = runningActual - runningTarget
        totalDifferences.append(difference)
    else:
        difference = ''
    data_matrix.append([gw,opponent,homeaway,targetPoints,actualPoints,runningTarget,runningActual,difference])

table = FF.create_table(data_matrix)
plotly.offline.plot(table, filename='Top_4_Table.html',auto_open=True)

## GRAPH ##
champions = Scatter(
    name='Champions (88pts)',
    line = dict(
        color = ('rgb(200,200,200)'),
        width=1
    ),
    x=[1,38],
    y=[0,14]
)

liverpoolX = []
liverpoolY = []

for d in range(len(totalDifferences)):
    liverpoolX.append(d)
    liverpoolY.append(totalDifferences[d])

liverpool = Scatter(
    name='Liverpool',
    line = dict(
        color = ('rgb(195,16,20)'),
        width=4
    ),
    x=liverpoolX,
    y=liverpoolY
)

data = Data([champions,liverpool])

layout = dict(title = 'Liverpool Road to Top Four',
              xaxis = dict(title='Gameweek<br><i>Liverpool are on course for a top four finish</i>' if totalDifferences[-1]>=0 else 'Gameweek<br><i>Not on course for top four this season</i>',autotick=False,tick0=1),
              yaxis = dict(title='Difference from top four finish',autotick=False,tick0=1)
)

plotly.offline.plot({
    "data": data,
    "layout": layout
},filename='Top_4_Graph.html',auto_open=True,show_link=False)

sleep(10)
remove('Top_4_Graph.html')
remove('Top_4_Table.html')
