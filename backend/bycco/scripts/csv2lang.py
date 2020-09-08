import csv
import json
import enum


def csv2lang():
    with open("backend/bycco/scripts/lang_all.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        allrows = []
        for r in reader:
            allrows.append(r)
    for l in ['en', 'fr', 'nl', 'de']:
        with open(f'frontend/src/util/{l}.js', 'w', encoding='utf8') as f:
        # with open(f'frontend/src/util/{l}.js', 'w', encoding='utf8') as f:
            f.write(f'const {l} = {{\n')
            for r in allrows:
                f.write(f'"{r["key"]}": "{r[l]}",\n')
            f.write('}\n')
            f.write(f'export default {l}')

if __name__ == '__main__':
    csv2lang()
    print('done')

