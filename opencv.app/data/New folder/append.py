from re import L
from requests import head


csv_file = [
    "1-linkedin.csv",
    "2-linkedin.csv",
    "3-linkedin.csv",
    "4-linkedin.csv",
    "5-linkedin.csv",
    "6-linkedin.csv",
]

output_file = "output.csv"

count = 0
for file in csv_file:
    print(file)
    with open(file, 'r', encoding='utf-8') as f:
        header = f.readline()
        if count == 0:
            with open(output_file + '.csv', 'w', encoding='utf-8') as f_out:
                f_out.write(header)
        
        lines = []
        for line in f:
            print(line)
            lines.append(line)

        with open(output_file + '.csv', 'a', encoding='utf-8') as f_out:
            f_out.writelines(line)
        count += 1
