import re
import numpy as np
import pandas as pd
class processor:
    contents = None
    processed = None

    def __init__(self):
        pass

    def setContents(self, contents):
        self.contents = contents

    def getTitles(self):
        if self.contents:
            titles = filter(lambda x:x.startswith('Title:'), self.contents)
            titles = map(lambda x:re.split('Title:',x)[1],titles)
            titles = map(lambda x:re.split('\r',x)[0], titles)
            return titles
        else:
            return None

    def getSources(self):
        if self.contents:
            comp = filter(lambda x: x.startswith('Source:'), self.contents)
            sources = map(lambda x: x[x.find('Source:')+7 : x.find('Volume:')],comp)
            return sources
        else:
            return None

    def getVolumes(self):
        comp = filter(lambda x: x.startswith('Source:'), self.contents)
        return map(lambda x:x[x.find('Volume:'):x.find('DOI:')-1], comp)

    def getRanks(self):
        maxDepth = 7
        result = []
        for i, line in enumerate(self.contents):
            if line.startswith('Addresses:'):
                result.append(i)

        ranks = np.array([np.array(map(lambda x: 1 if x else 0, [self.contents[i+j].find('Wuhan Inst Technol') > 0 for i in result]))*(j+1) for j in range(0,maxDepth)])
        ranks = ranks.T
        entityRanks = [min(np.array(filter(lambda y:y>0, item))) for i, item in enumerate(ranks)]
        return entityRanks

    def process(self):
        # res = np.array([np.array(self.getTitles()), np.array(self.getSources()), np.array(self.getVolumes()), np.array(self.getRanks())])
        df = pd.DataFrame(self.getTitles())
        df['sources'] = pd.DataFrame(self.getSources())
        df['volumes'] = pd.DataFrame(self.getVolumes())
        df['entityRanks'] = pd.DataFrame(self.getRanks())
        self.processed = df


