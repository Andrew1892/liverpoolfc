import plotly
from plotly.graph_objs import Scatter, Layout, Data
from plotly.tools import FigureFactory as FF
from os import remove
from time import sleep

fixtures = [
    ['A', 'Arsenal', 1.50],
    ['A', 'Burnley', 2.75],
    ['A', 'Tottenham', 1.50],
    ['H', 'Leicester', 2.50],
    ['A', 'Chelsea', 1.50],
    ['H', 'Hull', 3.00],
    ['A', 'Swansea', 2.25],
    ['H', 'Man United', 2.50],
    ['H', 'West Brom', 2.75],
    ['A', 'Crystal Palace', 1.75],
    ['H', 'Watford', 2.75],
    ['A', 'Southampton', 1.75],
    ['H', 'Sunderland', 3.00],
    ['A', 'Bournemouth', 2.25],
    ['H', 'West Ham', 2.75],
    ['A', 'Middlesbrough', 2.25],
    ['A', 'Everton', 1.50],
    ['H', 'Stoke', 3.00],
    ['H', 'Man City', 2.00],
    ['A', 'Sunderland', 2.75],
    ['A', 'Man United', 1.50],
    ['H', 'Swansea', 2.75],
    ['H', 'Chelsea', 2.50],
    ['A', 'Hull', 2.75],
    ['H', 'Tottenham', 2.25],
    ['A', 'Leicester', 1.75],
    ['H', 'Arsenal', 2.00],
    ['H', 'Burnley', 3.00],
    ['A', 'Man City', 1.50],
    ['H', 'Everton', 2.50],
    ['H', 'Bournemouth', 2.75],
    ['A', 'Stoke', 2.50],
    ['A', 'West Brom', 2.25],
    ['H', 'Crystal Palace', 2.75],
    ['A', 'Watford', 2.00],
    ['H', 'Southampton', 2.50],
    ['A', 'West Ham', 2.00],
    ['H', 'Middlesbrough', 2.75]
]

results = 'WLDWWWWDW'

alternativeTable = []
runningTarget=0
runningActual=0


# game score - how well you're doing based on what was expected
# par score - how far each team is on/off course for 88 points

for i in range(len(results)):
    res=results[i]
    tbl=fixtures[i]
    if res=='W':
        res=3
    elif res=='D':
        res=1
    else:
        res=0
    tbl.append(res)
    runningTarget+=tbl[2]
    runningActual+=res
    tbl.append(runningTarget)
    tbl.append(runningActual)
    alternativeTable.append(tbl)

for result in fixtures[len(alternativeTable):]:
    result.append('')
    result.append('')
    result.append('')
    alternativeTable.append(result)


## TABLE
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
plotly.offline.plot(table, filename='Champions_Table.html',auto_open=True)

## GRAPH
topFour = Scatter(
    name='Top Four (74pts)',
    line = dict(
        color = ('rgb(200,200,200)'),
        width=1
    ),
    x=[1,38],
    y=[0,-14]
)

liverpoolX = []
liverpoolY = []

for d in range(0,len(totalDifferences)):
    liverpoolX.append(d+1)
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

data = Data([topFour,liverpool])

layout = dict(title = 'Will Liverpool win the league?',
              xaxis = dict(title='Gameweek<br><br><i>Liverpool are on course to get {} points this season</i>'.format(int(88+totalDifferences[-1])),autotick=False,tick0=1),
              yaxis = dict(title='Difference from top four finish',autotick=False,tick0=1)
)

plotly.offline.plot({
    "data": data,
    "layout": layout
},filename='Champions_Graph.html',auto_open=True,show_link=False)


sleep(10)
remove('Champions_Graph.html')
remove('Champions_Table.html')
