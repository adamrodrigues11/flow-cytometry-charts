import flow
import pandas as pd


# note: need to find more elegant way to remove sd and mean aggregate from csv output
# TODOS:
# check that marker + and - data adds to 100% for each marker
# check that all combination data over all marker combinations adds to 100%
# aggregate the combination data
# generate plots


# def get_individual_markers(fields):
#     for i in range(10):  # can be a max number of individual markers determined by a reasonable limit
#         if len(fields) - (i * 2) == 2 ** i:
#             return fields[:i]
#     raise Exception('Fields are missing')


# def check_is_data_complete(samples, fields):
#     """Check to make sure each trial has data for each field.
#     """
#     for trials in samples.values():
#         for trial in trials:
#             assert len(trial) == len(fields)


# def check_pos_neg_complete(fields, samples):
#     markers = get_individual_markers(fields)
#     num_markers = len(markers)
#     for sample_id in samples:
#         for trial in samples[sample_id]:
#             for i in range(num_markers):
#                 pos_plus_neg = trial[i] + trial[i + num_markers]
#                 if not 99.9 < pos_plus_neg < 100.1:
#                     samples[sample_id].remove(trial)  # error maybe a result of aliasing????


def main():
    flow_data = flow.FlowData.from_flojo_csv('test.csv')
    print(flow_data)
    for sample_id, trials in flow_data.samples.items():
        print(sample_id)
        for trial in trials:
            print(trial)

if __name__ == '__main__':
    main()
