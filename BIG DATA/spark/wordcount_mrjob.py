from mrjob.job import MRJob, MRStep
import re

WORD_RE = re.compile(r"[\w]+")

class MRWordFreqCount(MRJob):
    def mapper1(self, _, line):
        for word in WORD_RE.findall(line):
            if len(word)>=5 :
                yield word.lower(), 1

    def combiner1(self, word, counts):
        yield word, sum(counts)

    def reducer1(self, word, counts):
        yield None, (sum(counts),word)

    def reducer2(self, _, compteur): 
        yield max(compteur)

    def steps(self):
        return [
           MRStep(mapper=self.mapper1,
                  combiner=self.combiner1,
                  reducer=self.reducer1),
           MRStep(reducer=self.reducer2)
        ]

if __name__ == '__main__' :
    MRWordFreqCount.run()
