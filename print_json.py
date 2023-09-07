import json
import pprint
import sys

def read_and_pprint_json(file_name):
  try:
    with open(file_name, 'r') as f:
      data = json.load(f)
    pprint.pprint(data)
  except FileNotFoundError:
    print(f"File {file_name} not found.")
  except json.JSONDecodeError:
    print(f"Error decoding JSON in {file_name}.")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python script.py <json_file_name>")
  else:
    file_name = sys.argv[1]
    read_and_pprint_json(file_name)
