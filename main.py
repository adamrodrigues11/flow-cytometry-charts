import csv
import pandas as pd

# note: need to find more elegant way to remove sd and mean aggregate from csv output
# TODOS:
# check that marker + and - data adds to 100% for each marker
# check that all combination data over all marker combinations adds to 100%
# aggregate the combination data
# generate plots


def read_data_from_csv(filename):
    with open(filename) as csvfile:
        csv_reader = csv.reader(csvfile)
        fields = csv_reader.__next__()[1:-1]  # ignore first and last column
        samples = {}
        for row in csv_reader:
            sample_id = row.pop()  # remove last column from row, and name it sample_id
            # ensure sample_id is not empty
            if not sample_id:
                continue
            trial = list(map(lambda x: float(x), row[1:]))  # ignore first column
            if sample_id not in samples:
                samples[sample_id] = [trial]
            else:
                samples[sample_id].append(trial)
        return fields, samples


def check_are_fields_complete(fields):
    """Check to make sure all markers have positive and negative columns, and that all boolean cases are covered
    """


def check_is_data_complete(samples, fields):
    """Check to make sure each trial has data for each field.
    """
    for trials in samples.values():
        for trial in trials:
            assert len(trial) == len(fields)


def main():
    fields, samples = read_data_from_csv('test.csv')
    # process fields
    fields = list(map(lambda x: x.split('/').pop().split('|')[0].strip(), fields))
    print(fields)
    check_are_fields_complete(fields)
    check_is_data_complete(samples, fields)


if __name__ == '__main__':
    main()
