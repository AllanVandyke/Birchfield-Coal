import json
import os
from dataFile import customerList

blendsRDC_Path = './BlendsRDC.json'


def update_blends(data: dict, file: str)-> None:
    if os.path.exists(file) and os.path.getsize(file) > 0:
        try:
            with open(file, 'r') as blends:
                fileData = json.load(blends)
                for item in data:
                    fileData.append(item)
            with open(file, 'w') as blends:
                json.dump(fileData, blends, indent=4)
                print(f"\nData written to {file} successfully.\n")
        except Exception as e:
            print(f"Error occurred while writing to file: {e}")
    else:
        try:
            with open(file, 'w') as blends:
                dataList = [data for data in customerList]
                json.dump(dataList, blends, indent=4)
            print(f"\nData written to {file} successfully.\n")
        except FileNotFoundError:
            print(f"File {file} not found.")

def check_blends(data: dict, file: str) -> None:
    if os.path.exists(file) and os.path.getsize(file) > 0:
        try:
            with open(file, 'r') as blends:
                fileData = json.load(blends)
                for item in data:
                    if item not in fileData:
                        update_blends([item], file)
                else:
                    print(f"\nAll items from data are already present in {file}.\n")
        except Exception as e:
            print(f"Error occurred while checking the file: {e}")
    else:
        update_blends(data, file)
    


if __name__ == '__main__':
    
    check_blends(customerList, blendsRDC_Path)

    
    
