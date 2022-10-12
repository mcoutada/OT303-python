from mrjob.job import MRJob
from mrjob.step import MRStep

# Create a new class and inherits from MRJob.
# Execute it locally: python3 mrjob_wordcount.py file.txt
# Execyte in hadoop:


class MRJWordCount(MRJob):

    def step(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer)
        ]

    # Mapper function
    def mapper(self, _, line):
        line = line.strip()
        words = line.split()
        for word in words:
            # Return key - value
            yield word, 1

    def reducer(self, key, value):
        # Key is the word, value is the sum of the values mapped.
        yield key, sum(value)


if __name__ == '__main__':
    # Run map and reduce.
    MRJWordCount.run()
