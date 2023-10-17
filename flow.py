import csv


# could abstract flow samples as a class to fully abstract the data structure

class FlowFields:
    def __init__(self, fields):
        # check to make sure that the fields all have pos/neg for each marker and all boolean gating combinations
        self.fields = fields

    def get_length(self):
        return len(self.fields)

    def __iter__(self):
        return iter(self.fields)

    def __str__(self):
        return str(self.fields)


class FlowTrial:
    def __init__(self, fields, values):
        # fields is a FlowFields obj (conforms to field constraints)
        assert fields.get_length() == len(values)  # ensure matches number of fields
        # also check proportions add properly here or discard/raise
        self.trial = dict(zip(fields, map(lambda x: float(x), values)))

    def __str__(self):
        return str(self.trial)

    def aggregate_gated_markers_data(self):
        pass


class FlowData:
    def __init__(self, fields, samples=None):
        # samples is a dictionary mapping sample ids to a collection of trials
        # fields are a list confirmed to adhere to field constraints
        self.fields = fields
        if samples is None:
            samples = {}
        self.samples = samples

    def __str__(self):
        fields_str = 'fields: ' + str(self.fields)
        samples_str = 'samples: ' + str(self.samples)
        return '\n'.join([fields_str, samples_str])

    def add_sample(self, sample_id, trials=None):
        if trials is None:
            trials = []
        if sample_id not in self.samples:
            self.samples[sample_id] = trials

    def get_trials(self, sample_id):
        return self.samples.get(sample_id)

    def add_trial(self, sample_id, trial):
        assert isinstance(trial, FlowTrial)
        trials = self.get_trials(sample_id)
        if trials is None:
            self.add_sample(sample_id, [trial])
        else:
            trials.append(trial)

    @staticmethod
    def from_flojo_csv(file_name):
        with open(file_name) as csvfile:
            csv_reader = csv.reader(csvfile)
            raw_fields = csv_reader.__next__()[1:-1]  # ignore first and last column
            fields = FlowFields(list(map(lambda x: x.split('/').pop().split('|')[0].strip(), raw_fields)))
            flow_data = FlowData(fields)
            for row in csv_reader:
                sample_id = row.pop()  # remove last column from row, and name it sample_id
                # guard that sample_id is not empty
                if not sample_id:
                    continue
                trial = FlowTrial(flow_data.fields, row[1:])  # ignore first column of csv row
                flow_data.add_trial(sample_id, trial)
            return flow_data

    def get_markers(self):
        return self.fields

    def get_num_markers(self):
        return len(self.fields)

    def aggregate_gated_markers_data(self):
        pass

