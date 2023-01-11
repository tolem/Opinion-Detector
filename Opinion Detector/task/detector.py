# write yor code here
import pandas as pd
opinion = {"Review": [], "Score": []}
file_name = input()
line_number = 0
with open('%s' % file_name, 'r', encoding="UTF-8") as file:
    while line_number < 150000:
        line = file.readline()
        line = line.strip()
        line_number = line_number + 1
        if len(line) > 0:
            score = line[-2:] if line[-2].isdigit() else line[-1:]
            last = -2 if line[-2].isdigit() else -1
            opinion['Review'].append(line[:last])
            opinion['Score'].append(score.rstrip())

    else:
        df = pd.DataFrame(data=opinion)
        print(df.head(), df.tail(), sep='\n')

# dframe = pd.read_csv(input(), sep=None, header=None)
# dframe.columns = ['Review', 'Score']
#
# dframe['Review'] = dframe['Review'].apply(lambda x: f"\" {x.strip()} \"")
# dframe['Score'] = dframe['Score'].apply(lambda x: x[x.index(",") + 1:].strip())
#
# print(dframe[:5])
# print(dframe[-5:])