#Behavioral Risk Factors Data--Health Related Quality of Life

#NOTE: Required packages (all from pip): reportlab, geos, https://github.com/matplotlib/basemap/archive/v1.1.0.tar.gz
#also required proj, installed with homebrew

#set up the output doc
#we're using reportlab for this pdf
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
import os

#terminal start
linebreak = '--------'
print linebreak

#create the pdf, which we'll call 'behavioralRiskFactorDataHealthRelatedQualityOfLife'
doc = SimpleDocTemplate('behavioralRiskFactorDataHealthRelatedQualityOfLife.pdf', pagesize=letter)

#for organizations sake, we make a list w/every object we're putting into our pdf
elements = []
#also create space for the aesthetic
space = .1 * inch

#let's get a title in
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=18,)
elements.append(Paragraph('Beahvioral Risk Factors Data: Health-Related Quality of Life', style))
#some space
elements.append(Spacer(1, 4 * space))

#let's describe our goals in Part 1 to the person reading the PDF
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=16,)
elements.append(Paragraph('Analysis Part 1: How are people being affected by their poor health?',style))
elements.append(Spacer(1, 2 * space))
#style for Big Question
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=14,)
elements.append(Paragraph('Big Questions:',style))
elements.append(Spacer(1, space))
#new style for questions
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=12,)
elements.append(Paragraph('1-How is the average person affected by their health?',style))
elements.append(Spacer(1, space))
elements.append(Paragraph('''2-How many people are most affected by their poor
health, and how much are they affected?''',style))
elements.append(Spacer(1,space))
elements.append(Paragraph('''3-How many people think that they have poor health,
and how does this compare to relatively objective numbers?''',style))
elements.append(Spacer(1, 3*space))


import pandas as pd
import numpy as np
#load; a big csv, so set low_memory to False to avoid warnings (warning to any users w/low memory)
d = pd.read_csv('behavioralRiskFactorDataHealthRelatedQualityOfLife.csv',low_memory=False)
#test
print linebreak
print "Test: Head"
d.head()

#list of questions
q = []

for i in d.Question:
    #factor out repeats
    if i not in q:
        q.append(i)

#pretty print to console: this is just diagnostic confirmation that the code is working
print linebreak
print "Test Questions:"
for n,i in enumerate(q):
    print '%d) %s.'%(n+1,i)

#let's describe this part to our reader
#no need to change text, still body under pt. 1
elements.append(Paragraph('Q: How is the average person affected by their health?',style))
elements.append(Spacer(1,space))
elements.append(Paragraph('''A: We will answer this through analysis of mean
days of activity limitation, mean mentally unhealthy days, mean physically or
mentally unhealthy days, and mean physically unhealthy days.''',style))
elements.append(Spacer(1,2*space))

#Limited Activity
avgData = {}
import math

activityLim = d[d.Question == 'Mean days of activity limitation']

sm = 0
n=0

for i in activityLim['Data_Value']:
    #filter out empty spaces in csv
    if not math.isnan(i):
        sm+=float(i)
        n+=1.0

avgActivityLim = sm/n
print linebreak
print "average of mean days of activity limitation: %f"%(avgActivityLim)
avgData['Activity Limitation'] = avgActivityLim

#Mentally Unhealthy days
mentalLim = d[d.Question == 'Mean mentally unhealthy days']
sm = 0
n=0

for i in mentalLim['Data_Value']:
    #filter out empty spaces in csv
    if not math.isnan(i):
        sm+=float(i)
        n+=1.0

avgMentalLim = sm/n
print linebreak
print "average of mean days of mental limitation: %f"%avgMentalLim

avgData['Mentally unhealthy'] = avgMentalLim

#Physically Unhealthy Days
physicalLim = d[d.Question == 'Mean physically unhealthy days']

sm = 0
n=0

for i in physicalLim['Data_Value']:
    #filter out empty spaces in csv
    if not math.isnan(i):
        sm+=float(i)
        n+=1.0

avgPhysicalLim = sm/n
print linebreak
print "average of mean days of physical limitation: %f"%avgPhysicalLim

avgData['Physically unhealthy'] = avgPhysicalLim

#Let's look at what this data shows us
import matplotlib.pyplot as plt
plt.bar(range(len(avgData)), avgData.values(), align='center')
plt.xticks(range(len(avgData)), avgData.keys())
plt.ylabel('Days of Limitation')
#these all have to be different lines because reportlab is finicky
plt.savefig('healthLimits.png')
img = Image('healthLimits.png')
img._restrictSize(50 * space, 50 * space)
elements.append(img)
os.remove('healthLimits.png')
plt.clf()

#let's write out a few conclusions from this graph
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=14,)
elements.append(Paragraph('Conclusions',style))
elements.append(Spacer(2,space))
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=12,)
elements.append(Paragraph('1-No significant amount of days lost from any category.',style))
elements.append(Spacer(1,space))
elements.append(Paragraph('2-Physically unhealthy days more than mentally unhealthy days.',style))
elements.append(Spacer(1,space))
elements.append(Paragraph('3-Very few days of activity limitation, overall.',style))
#works out, aesthetically, to go to the next page
elements.append(PageBreak())

#now, we'll write out the next bit we're focusing on
elements.append(Paragraph('''Q: How many people are most affected by their poor
health, and how much are they affected?''',style))
elements.append(Spacer(1,space))
elements.append(Paragraph('''A: We will answer this through analysis of
percentage with 14 or more activity limitation days, percentage with 14 or more
mentally unhealthy days (Frequent Mental Distress), and percentage with 14 or
more physically unhealthy days.''',style))
elements.append(Spacer(1,2*space))

#percentage w/14+ activity limitation days
extData = {}

highActivityLim = d[d.Question == 'Percentage with 14 or more activity limitation days']

sm = 0
n=0

for i in highActivityLim['Data_Value']:
    #filter out empty spaces in csv
    if not math.isnan(i):
        sm+=float(i)
        n+=1.0

avgHighActivityLim = sm/n
print linebreak
print "Percentage with 14 or more activity limitation days: %f"%avgHighActivityLim

extData['Activity Limitation'] = avgHighActivityLim

#Percentage with 14 or more mentally unhealthy days

highMentalLim = d[d.Question == 'Percentage with 14 or more mentally unhealthy days (Frequent Mental Distress)']

sm = 0.0
n = 0.0
for i in highMentalLim['Data_Value']:
    #filter out empty spaces in csv
    if not math.isnan(i):
        sm+=float(i)
        n+=1.0

avgHighMentalLim = sm/n
print linebreak
print '''Percentage with 14 or more mentally unhealthy days (Frequent Mental Distress)" %f"'''%avgHighMentalLim

extData['Mental Limitation'] = avgHighMentalLim

#Percentage with 14 more physically unhealthy days

highPhysicalLim = d[d.Question == 'Percentage with 14 or more physically unhealthy days']

sm = 0
n=0

for i in highPhysicalLim['Data_Value']:
    #filter out empty spaces in csv
    if not math.isnan(i):
        sm+=float(i)
        n+=1.0

avgHighPhysicalLim = sm/n
print linebreak
print 'Percentage with 14 or more physically unhealthy days: %f'%avgHighPhysicalLim

extData['Physical Limitation'] = avgHighPhysicalLim
plt.bar(range(len(extData)), extData.values(), align='center')
plt.xticks(range(len(extData)), extData.keys())
plt.ylabel('Percentage of Population')
plt.savefig('extremeLims.png')
img = Image('extremeLims.png')
img._restrictSize(50 * space, 50 * space)
elements.append(img)
os.remove('extremeLims.png')
plt.clf()

#let's write out a few conclusions from this graph
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=14,)
elements.append(Paragraph('Conclusions',style))
elements.append(Spacer(1,2*space))
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=12,)
elements.append(Paragraph('''1-Activity limitation minimal--few people
suffer from it.''',style))
elements.append(Spacer(1,space))
elements.append(Paragraph('''2-Not a big difference between mental and physical
limitation.''',style))
elements.append(Spacer(1,space))
elements.append(Paragraph('''3-Those who suffer do so greatly--14 is
significantly more than 3.5, the max suffered by the average person, and 10%
is still a significant amount of the population. There's clearly room for
improvement.''',style))
#consistency: next page
elements.append(PageBreak())

#now, we'll write out the next bit we're focusing on
elements.append(Paragraph('''Q: How many people think that they have poor
health, and how does this compare to relatively objective numbers?''',style))
elements.append(Spacer(1,space))
elements.append(Paragraph('''A: We will answer this through analysis of
percentage with fair or poor self-rated health.''',style))
elements.append(Spacer(1,2*space))

sRep = d[d.Question == 'Percentage with fair or poor self-rated health']

sm = 0
n=0

for i in sRep['Data_Value']:
    #filter out empty spaces in csv
    if not math.isnan(i):
        sm+=float(i)
        n+=1.0

avgSRep = sm/n
print linebreak
print "Percentage with fair or poor self-rated health: %f"%avgSRep

xVals = extData.values()
yVals = extData.keys()

xVals.append(avgSRep)
yVals.append('Self-Reported')

plt.bar(range(len(extData)+1), xVals,.3)
plt.xticks(range(len(extData)+1), yVals)
plt.ylabel('Percentage of Population')
plt.savefig('selfRate.png')
img = Image('selfRate.png')
img._restrictSize(50 * space, 50 * space)
elements.append(img)
os.remove('selfRate.png')
plt.clf()

#let's write out a few conclusions from this graph
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=14,)
elements.append(Paragraph('Conclusions',style))
elements.append(Spacer(1,2*space))
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=12,)
txt = '''1-More people self-report poor health than suffer from mental or
physical health limitations.'''
elements.append(Paragraph(txt,style))
elements.append(Spacer(1,space))
elements.append(Paragraph('2-Implies obsession with health and wellness',style))
elements.append(Spacer(1,space))

#spacing: now for our final conclusions from part 1
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=14,)
elements.append(Paragraph('Insights from Part 1:',style))
elements.append(Spacer(1,2*space))
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=12,)
txt = '''The average person doesn't lose much from poor health, in terms of days
 made inactive, etc. due to suffering.'''
elements.append(Paragraph('1-%s'%txt,style))
elements.append(Spacer(1,space))
txt = '''There are a not-inconsiderable amount of people who do lose a lot from
poor health; though they are relatively few, their loss is significant.'''
elements.append(Paragraph('2-%s'%txt,style))
elements.append(Spacer(1,space))
txt = '''More people believe that they belong to this category than actually do,
leaning toward the conclusion of some sort of nation-wide hypochondiracy.
'''
elements.append(Paragraph("3-%s"%txt,style))
elements.append(PageBreak())

#now, let's go to part 2 of our analysis
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=16,)
elements.append(Paragraph('Analysis Part 2: Health differences',style))
elements.append(Spacer(1, 2 * space))
#style for Big Question
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=14,)
elements.append(Paragraph('Big Questions:',style))
elements.append(Spacer(1, space))
#new style for questions
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=12,)
elements.append(Paragraph('1-How does health differ by state?',style))
elements.append(Spacer(1, space))
elements.append(Paragraph('2-How does health differ by age group?',style))
elements.append(Spacer(1, space))
elements.append(Paragraph('3-How does health differ by race?',style))
elements.append(Spacer(1, space))
elements.append(Paragraph('4-How does health differ by biological sex?',style))
elements.append(Spacer(1, 3*space))


#a dictionary of dictionaries to get more info on states
states = {}
#first, get a list of all states
for i in d['LocationAbbr']:
    if i not in states:
        states[i] = {}

#note: there are 52 states here because we're counting DC + puerto rico
print len(states.keys())
#one time diagnostic--double check our dict is properly compiled
#print states

#print a warning: this is a large dataset, and will take a while
print linebreak
print "This is going to take a minute. Just hang tight."

#for every state
for state in states.keys():
    #get the mean values for each data point
    for question in q:
        states[state][str(question)] = d[(d['LocationAbbr']==state)
        &(d['Question']==question)]['Data_Value'].mean()

#large and confusing in a terminal only print once for diagnostic purposes
#print states
#as dictionary doesn't have a head(), let's print just an example state
print states['NY']

#let's warn the terminal what we're doing
print linebreak
print "We're drawing maps, this could take a minute."

#display this data in a map
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

#setup

#standard color deviation
startColor = '585858'

#copy-pasted from the internet
stateAbbr = {
        'AK': 'Alaska','AL': 'Alabama','AR': 'Arkansas','AS': 'American Samoa',
        'AZ': 'Arizona','CA': 'California','CO': 'Colorado','CT': 'Connecticut',
        'DC': 'District of Columbia','DE': 'Delaware','FL': 'Florida','GA':
        'Georgia','GU': 'Guam','HI': 'Hawaii','IA': 'Iowa','ID': 'Idaho',
        'IL': 'Illinois','IN': 'Indiana','KS': 'Kansas','KY': 'Kentucky',
        'LA': 'Louisiana','MA': 'Massachusetts','MD': 'Maryland','ME': 'Maine',
        'MI': 'Michigan','MN': 'Minnesota','MO': 'Missouri','MS':
        'Mississippi','MT': 'Montana','NA': 'National','NC': 'North Carolina',
        'ND': 'North Dakota','NE': 'Nebraska','NH': 'New Hampshire',
        'NJ': 'New Jersey','NM': 'New Mexico', 'NV': 'Nevada','NY': 'New York',
        'OH': 'Ohio','OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania',
        'PR': 'Puerto Rico','RI': 'Rhode Island','SC': 'South Carolina',
        'SD': 'South Dakota','TN': 'Tennessee', 'TX': 'Texas','UT': 'Utah',
        'VA': 'Virginia','VI': 'Virgin Islands','VT': 'Vermont',
        'WA': 'Washington','WI': 'Wisconsin','WV': 'West Virginia',
        'WY': 'Wyoming'
        }

#the questions we're actually going to bother answering
questions = ['Mean days of activity limitation','Mean mentally unhealthy days',
            'Mean physically unhealthy days',
            'Percentage with 14 or more activity limitation days',
            'Percentage with 14 or more mentally unhealthy days (Frequent Mental Distress)',
            'Percentage with 14 or more physically unhealthy days',
            'Percentage with fair or poor self-rated health']

#and let's give a brief description of what the colors mean
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=14,)
elements.append(Paragraph('Location Data.',style))
elements.append(Spacer(1, space))
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=12,)
elements.append(Paragraph('''The brighter and more blue the color, the higher
the number.''',style))
elements.append(Spacer(1, space))

for question in questions:

    # create the map base
    map = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

    # add the states to the map
    map.readshapefile('st99_d00', name='states', drawbounds=True)

    # collect the state names from the shapefile attributes so we can
    # look up the shape obect for a state by it's name
    state_names = []
    for shape_dict in map.states_info:
        state_names.append(shape_dict['NAME'])

    ax = plt.gca() # get current axes instance

    # get each state, and fill the color in depending on it's numbers
    for i in states.keys():
        #for some reason, they have put US in as a key. this is weird.
        if not i == 'US':
            seg = map.states[state_names.index(stateAbbr[i])]
            #change
            n = int(hex(int(1000*states[i][question])),16)
            #add to start
            color = hex(int(startColor,16) + n)
            ## to recognize hex, 2: bc python puts 0x at start of hex object
            color = "#" + str(color)[2:]
            poly = Polygon(seg, facecolor=color,edgecolor='black')
            ax.add_patch(poly)

    plt.title(question)

    plt.savefig('map.png')
    img = Image('map.png')
    img._restrictSize(50 * space, 50 * space)
    elements.append(img)
    os.remove('map.png')
    plt.clf()

#let's write out a few conclusions from this section
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=14,)
elements.append(Paragraph('Conclusions',style))
elements.append(Spacer(1,2*space))
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=12,)
txt = '''1-Higher frequencies of each category tend to occur in the east coast
states and California. This may have less to do with actual occurence and more
to do with general medical practice and, perhaps, population. Or maybe cities
are just dirty and unhealthy.'''
elements.append(Paragraph(txt,style))
elements.append(Spacer(1,space))
txt = '''2-The states that have lower actual occurences of each category also
have less self-reported occurences. This is interesting, as it means that, as
actual occurences go up, self-reported occurences go up at a higher rate.'''
elements.append(Paragraph(txt,style))

#no page break--messes up format

style = ParagraphStyle(name='Normal',fontName='Times',fontSize=14,)
elements.append(Paragraph('Other Data',style))
elements.append(Spacer(1, space))
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=12,)
elements.append(Spacer(1, 2*space))

#dictionary of dictionaries
#a special exception to the years rule
ageList = []
ages = {}
raceList = []
races = {}
sexList = ['Male','Female']
sexes = {}
#Break_Out is a mess of things; let's clean it up a bit
for i in d['Break_Out']:
    if 'years' in i or i == '75+':
        if i not in ageList:
            ageList.append(i)
    elif i not in sexList and i not in raceList and not i == 'Overall':
        raceList.append(i)

for question in questions:
    ages[question] = {}
    sexes[question] = {}
    races[question] = {}


#diagnostic
print linebreak
print "ages"
print ageList
print "races"
print raceList
print "sexes"
print sexList

#print a warning: this is a large dataset, and will take a while
print linebreak
print "That's a lot of data! We just need a minute here."

#for every age group
for age in ageList:
    #get the mean values for each data point
    for question in questions:
        ages[str(question)][age] = d[(d['Break_Out']==age)
        &(d['Question']==question)]['Data_Value'].mean()

#races
for race in raceList:
    #get the mean values for each data point
    for question in questions:
        races[str(question)][race] = d[(d['Break_Out']==race)
        &(d['Question']==question)]['Data_Value'].mean()

#sexes
for sex in sexList:
    #get the mean values for each data point
    for question in questions:
        sexes[str(question)][sex] = d[(d['Break_Out']==sex)
        &(d['Question']==question)]['Data_Value'].mean()

#print a sample from each
print '[Mean mentally unhealthy days][75+]'
print ages['Mean mentally unhealthy days']['75+']

print '[Mean mentally unhealthy days][hispanic]'
print races['Mean mentally unhealthy days']['Hispanic']

print '[Mean mentally unhealthy days][female]'
print sexes['Mean mentally unhealthy days']['Female']

#let's make some bar graphs

#warning to the terminal
print linebreak
print "We're making bar graphs, hang tight!"

for question in questions:
    style = ParagraphStyle(name='Normal',fontName='Times',fontSize=12,)
    elements.append(Paragraph(question,style))

    plt.bar(range(len(ages[question])), ages[question].values())
    plt.xticks(range(len(ages[question])), sorted(ages[question].keys()), rotation=15)
    #we have a lot of info, let's make some space for it
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.title("Distribution of Ages: %s"%question)
    plt.savefig('ages.png')
    img = Image('ages.png')
    img._restrictSize(50 * space, 50 * space)
    elements.append(img)
    os.remove('ages.png')
    plt.clf()

    elements.append(Spacer(1, space))

    plt.bar(range(len(races[question])), races[question].values(),
    align='center')
    plt.xticks(range(len(races[question])), races[question].keys(), rotation=45)
    plt.title("Distribution of Races: %s"%question)
    #it's a tight squeeze for x-labels
    plt.tight_layout()
    plt.savefig('races.png')
    img = Image('races.png')
    img._restrictSize(50 * space, 50 * space)
    elements.append(img)
    os.remove('races.png')
    #close to clear tight_layout
    plt.close()

    elements.append(Spacer(1, 2*space))

    plt.bar(range(len(sexes[question])), sexes[question].values(),
    align='center')
    plt.xticks(range(len(sexes[question])), sexes[question].keys())
    plt.title("Distribution of Sexes: %s"%question)
    plt.savefig('sexes.png')
    img = Image('sexes.png')
    img._restrictSize(50 * space, 50 * space)
    elements.append(img)
    os.remove('sexes.png')
    plt.clf()

#our conclusions from part 2
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=14,)
elements.append(Paragraph('Insights from Part 1:',style))
elements.append(Spacer(1,2*space))
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=12,)
txt = '''Highest physical health issues not among 75+, but 65-74 year old crowd. And
even then, not by much. Mental health issues, unsurprisingly, dominated by the
18-24 crowd, but again, not by the percentage you would expect. Perhaps age
isn't as big a factor as I thought'''
elements.append(Paragraph("1-%s"%txt,style))
elements.append(Spacer(1,space))
txt = '''Native American/Alaskan Native doing worse by a lot in every category.
Asian/Pacific Islander doing best. All other races sort of the same.'''
elements.append(Paragraph("2-%s"%txt,style))
elements.append(Spacer(1,space))
txt = '''Females always a percent or two above males in terms of lack of health.
Not a large of distinction to be stastistcally signifcant, given the imprecise
data.'''
elements.append(Paragraph("3-%s"%txt,style))
elements.append(PageBreak())

#now, let's go to part 3 of our analysis
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=16,)
elements.append(Paragraph('Analysis Part 3: Health Changes Over Time',style))
elements.append(Spacer(1, 2 * space))

#lets check out some years
yrs = [int(x) for x in d['Year'].unique() if str(x) != 'nan']
#make sure it worked
print linebreak
print "years:"
print yrs

#shaking things up with a dictionary of lists
years = {}
for question in questions:
    years[question] = [[],[]]
    temp = {}
    for yr in yrs:
        temp[yr] = d[(d['Year']==yr)&(d['Question']==question)]['Data_Value'].mean()
    for yr in sorted(yrs):
        years[question][0].append(yr)
        years[question][1].append(temp[yr])

#how did that work out
print "years data for Mean mentally unhealthy days:"
print years['Mean mentally unhealthy days']

print linebreak

from matplotlib.ticker import MaxNLocator

for question in questions:
    plt.plot(years[question][0],years[question][1])
    plt.title(question)
    #because 2002.5 is not a real year, and matplot won't convince me otherwise
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.savefig('line.png')
    img = Image('line.png')
    img._restrictSize(50 * space, 50 * space)
    elements.append(img)
    os.remove('line.png')
    plt.clf()

#now for our final conclusions from part 3
style = ParagraphStyle(name='Normal',fontName='Times',fontSize=14,)
elements.append(Paragraph('Insights from Part 3:',style))
elements.append(Spacer(1,2*space))

#one, long conclusion instead of a bunch of smaller ones
#because of nature of Part 3 analysis
conc = ''' While all numbers have gone up (unsurprising, as medicine evolves),
poor self-reported health seems to have risen much more, particularly around
the year 2000. We can likely attribute this, at least in part, to the rise of
internet self-diagnosis, from websites such as WebMD, and likely means good
things for our market. If people trust the internet to diagnose them, certainly
they'll trust AI.
'''

style = ParagraphStyle(name='Normal',fontName='Times',fontSize=12,)
elements.append(Paragraph(conc,style))
elements.append(Spacer(1,space))
elements.append(Paragraph('''There's a weird dip in 2002 that I can't account
for. 2002 was a bad year for health.''',style))

#make the pdf
doc.build(elements)
