import pandas as pd

# 读取 Excel 文件
input_file = '铁矿_全球到港_分品种_20240506.xlsx'
df = pd.read_excel(input_file)


# 增加一个条件，装货国不是中国的行保留
df_filtered = df[df['到货国'] != '中国']
df_filtered_delete = df[df['到货国'] == '中国']

# 输出到 Excel 文件

output_file_delete = input_file + '_海漂_根据到货国被删除.xlsx'
df_filtered_delete.to_excel(output_file_delete, index=False)

output_file = input_file + '_海漂_根据到货国删除后.xlsx'
df_filtered.to_excel(output_file, index=False)


