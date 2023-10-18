import flow
import pandas as pd


# note: need to find more elegant way to remove sd and mean aggregate from csv output ??
# TODOS:
# aggregate the combination data
# generate plots
# move the hardcoded number of markers to a command line arg


def main():
    flow_data = flow.DataSet.from_flojo_csv('test.csv', 5)
    print(flow_data)
    for sample_id, trials in flow_data.samples.items():
        print(sample_id)
        for trial in trials:
            print(trial)


if __name__ == '__main__':
    main()
