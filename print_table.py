import json
import pprint
import sys

import pandas as pd

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

def get_comparison_type(key):

  if key.startswith('adam'):
    optimizer = 'Adam'
    if key == 'adam':
      identifier = ''
    else:
      identifier = key.split('adam_')[1]
  elif key.startswith('sgd'):
    optimizer = 'SGD + Momentum'
    if key == 'sgd':
      identifier = ''
    else:
      identifier = key.split('sgd_')[1]
  else:
    return None, None

  prettify_identifier = {
    'jitter': 'Jitter',
    'no_warp': 'No Warp', # probably won't use this
    'scaledown': 'Scaledown',
    '': 'Default'
  }

  return optimizer, prettify_identifier[identifier]

def get_max_key_val(dct):

  max_val = max(int(k) for k in dct)
  return dct[str(max_val)]


def get_table(data):

  df_list = []

  for key, results in data.items():
    res_dict = {}
    optimizer, comparison_type = get_comparison_type(key)
    if optimizer is None or comparison_type == 'No Warp':
      continue
    res_dict['Optimizer'] = optimizer
    res_dict['Comparison Type'] = comparison_type
    res_dict['Change Point Sequence Agreement'] = results['exact_correct_sequences_proportion']
    res_dict['Compressed Change Point Sequence Agreement'] = results['correct_sequences_proportion']
    res_dict['Average Change Point Error'] = results['average_exact_step_count_error']
    weight_alignment = results['distance_metric']
    res_dict['Weight Alignment Error'] = get_max_key_val(weight_alignment)
    quantized_agreement = results['distance_metric']
    res_dict['Quantized Weight Agreement'] = get_max_key_val(quantized_agreement)
    res_dict['Validation Accuracy Correlation'] = results['val_accuracy_correlation']
    res_dict['Validation Loss Correlation'] = results['val_loss_correlation']
    res_dict['Inference Agreement'] = results['inference_agreement_proportion']
    res_dict['Incorrect Inference Agreement'] = results['incorrect_inference_agreement_proportion']
    res_dict['$\hat Q$ model Accuracy'] = results['quantizer_model_accuracy']
    res_dict['STE model Accuracy'] = results['initializer_model_accuracy']
    df_list.append(res_dict)

  df = pd.DataFrame(df_list)  
  
  order = {
    'Default': 1,
    'Jitter': 2,
    'Scaledown': 3,
  }

  df['order'] = df['Comparison Type'].map(order)
  df = df.sort_values(by='order').drop(columns='order')
  df = df.sort_values(by='Optimizer', ascending=False)

  return df  


if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python print_table.py <json_file_name>")
    sys.exit()

  file_name = sys.argv[1]
  data = read_json(file_name)
  df = get_table(data).set_index(['Optimizer', 'Comparison Type'])

  df = df.T
  df = df.reset_index().rename(columns={'index': 'Metric'}).set_index('Metric')

  print(df)
  num_columns = len(df.columns) + 1
  column_format = "|".join(["c"] * num_columns)
  column_format = f"|{column_format}|"

  latex_output = df.to_latex(
    float_format="%.3f", 
    index=True, 
    column_format=column_format, 
    header=True, 
    bold_rows=True)

  latex_output = latex_output.replace('\\toprule', '')
  latex_output = latex_output.replace('\\\\', '\\\\ \\hline')
  latex_output = latex_output.replace('\\midrule', '')
  latex_output = latex_output.replace('\\bottomrule', '')

  # Center-align multicolumn headers
  latex_output = latex_output.replace('{r}', '{c}')
  print(latex_output)


