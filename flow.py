import csv
import math
import matplotlib as plt


def is_valid_field_list(fields, num_markers):
    # quick check to make sure that the fields all have pos/neg for each marker and all boolean gating combinations
    return len(fields) == num_markers * 2 + 2 ** num_markers


def is_valid_trial(trial, fields):
    # check to make sure all the pos/neg pairs and bool gate proportions add to 100%
    pairs = zip(fields.pos_markers, fields.neg_markers)
    return all([math.isclose(trial[pos] + trial[neg], 100.0, rel_tol=1e-2) for pos, neg in pairs]) and (
        math.isclose(sum([trial[field] for field in fields.bool_gates]), 100.0, rel_tol=1e-2)
    )


class Fields(list):
    def __init__(self, fields, num_markers):
        assert is_valid_field_list(fields, num_markers)
        super().__init__(fields)
        self.pos_markers = self[:num_markers]
        self.neg_markers = self[num_markers: num_markers * 2]
        self.bool_gates = self[num_markers * 2:]


class Trial(dict):
    def __init__(self, fields, values):
        # fields is a FlowFields obj (conforms to field constraints)
        assert len(fields) == len(values)  # ensure a value for every field
        trial = dict(zip(fields, map(lambda x: float(x), values)))
        if not is_valid_trial(trial, fields):
            raise Exception(f"Rejected invalid trial: {trial}")
        super().__init__(trial)

    def aggregate_gated_markers_data(self):
        pass


class DataSet:
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
        assert isinstance(trial, Trial)
        trials = self.get_trials(sample_id)
        if trials is None:
            self.add_sample(sample_id, [trial])
        else:
            trials.append(trial)

    @staticmethod
    def from_flojo_csv(file_name, num_markers):
        with open(file_name) as csvfile:
            csv_reader = csv.reader(csvfile)
            raw_fields = csv_reader.__next__()[1:-1]  # ignore first and last column
            fields = Fields(list(map(lambda x: x.split('/').pop().split('|')[0].strip(), raw_fields)), num_markers)
            flow_data = DataSet(fields)
            for row in csv_reader:
                sample_id = row.pop()  # remove last column from row, and name it sample_id
                # guard that sample_id is not empty
                if not sample_id:
                    continue
                try:
                    trial = Trial(flow_data.fields, row[1:])  # ignore first column of csv row
                    flow_data.add_trial(sample_id, trial)
                except Exception as e:
                    print(sample_id, e)

            return flow_data

    def get_num_markers(self):
        return len(self.fields.pos_markers)

    def aggregate_gated_markers_data(self):
        pass

    def generate_plots(self):
        pass
