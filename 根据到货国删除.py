import pandas as pd

# 读取 Excel 文件
input_file = '/Users/minggong/PycharmProjects/pythonProject/铁矿_全球到港_分品种_20240506.xlsx'
df = pd.read_excel(input_file)

# 首先根据国家和到货国不相等的条件过滤数据
df_filtered = df[df['国家'] != df['到货国']]

# 增加一个条件，装货国不是中国的行保留
df_filtered = df_filtered[df_filtered['到货国'] != '中国']

# 输出到 Excel 文件

output_file = input_file + '_根据到货国删除后.xlsx'
df_filtered.to_excel(output_file, index=False)
