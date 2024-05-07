import pandas as pd

# 读取 Excel 文件
input_file = '/Users/minggong/PycharmProjects/pythonProject/铁矿_全球到港_分品种_20240506.xlsx'
df = pd.read_excel(input_file)

# 删除满足条件的行，即当H列和M列的值相等时
df_filtered = df[df['国家'] != df['到货国']]

# 保存筛选后的结果到新的 Excel 文件
output_file = '铁矿_全球到港_分品种_20240506.xlsx-delete.xlsx'
df_filtered.to_excel(output_file, index=False)

print(f"Filtered data saved to '{output_file}'")
