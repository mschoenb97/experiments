import json
import pprint
import sys

from matplotlib import pyplot as plt

import pandas as pd

plt.style.use('ggplot')


def read_json(file_name):
  try:
    with open(file_name, 'r') as f:
      data = json.load(f)
  except FileNotFoundError:
    print(f"File {file_name} not found.")
  except json.JSONDecodeError:
    print(f"Error decoding JSON in {file_name}.")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
  
  return data

def process_for_plot(dct):

  x = []
  y = []

  for key, val in dct.items():
    x.append(int(key))
    y.append(val)

  return x, y

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python weight_metric_plot.py <json_file_name>")
    sys.exit()

  file_name = sys.argv[1]
  data = read_json(file_name)

  sgd_data = data['sgd']['distance_metric']
  sgd_no_warp_data = data['sgd_no_warp']['distance_metric']

  x, y = process_for_plot(sgd_data)
  plt.plot(x, y, label='Default SGD')
  x, y = process_for_plot(sgd_no_warp_data)
  plt.plot(x, y, label='SGD without re-initializing')
  plt.ylabel('Weight Alignment Error')
  plt.xlabel('Epoch')
  plt.title("Effect of Weight Initialization on Weight Alignment")
  plt.legend()

  plt.savefig('run_5/weight_alignment_sequence.png')



