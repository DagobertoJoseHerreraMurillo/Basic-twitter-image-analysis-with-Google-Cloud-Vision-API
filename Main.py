from Lab6opt import ImageDownloader
from os import listdir
from os.path import isfile, join
from Lab6opt import label
import plotly
import shutil



##############
# PARAMETERS #
##############
user = "nytimes"
numberOfPhotos = 100
path = "/"
includeRT = True
IncludeReplies = True
##############


#DELETE FOLDER
shutil.rmtree(path)


#Download the images
ImageDownloader.main(user, includeRT, IncludeReplies, numberOfPhotos, path)

# Get elements in path
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

# Create an array with all the photos' paths
files = []
for i in onlyfiles:
    files.append(path + "/" + i)


tags = []
tuple = []
# Send the images to google
for pht in files:
    response = label.main(pht)
    # Store the tags
    for result in response['responses'][0]['labelAnnotations']:
        # parseResult = "%s - %.3f" % (result['description'], result['score'])
        tuple = [result['description'], result['score']]
        tags.append(tuple)


#############################################################################
# We want to count the number of times a tag appears in the tags list
# then, with the tag and the amount of times it appears, create the graph
#############################################################################

# convert the two dimensional list in a list with only tags:
justNames = []
for i in tags:
    justNames.append(i[0])

# create a set of the list, which contains only the unique values
my_set = set(justNames)
setList = list(my_set)

# Now, we can iterate the set list, counting the number of times one element appears in the list:
listOfTags = []
coutOfTags = []
for i in setList:
    listOfTags.append(i)
    coutOfTags.append(justNames.count(i))

# Once we have our final result, we just need to create the plot

# Sort the results
coutOfTags, listOfTags = zip(*sorted(zip(coutOfTags, listOfTags)))

#Print it using plotly
plotly.offline.plot({
"data": [
    plotly.graph_objs.Bar(x=coutOfTags,y=listOfTags, orientation = 'h')
]
})


