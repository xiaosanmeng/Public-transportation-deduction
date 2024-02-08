import pandas as pd
################################
# 需要下载包pandas配置到解释器环境之中
# 源路径需要csv数据
# 编码方式采用GB2312，便于使用Excel打开
################################


source_path = 'source_data.csv'
destination_path = 'version7_merged_data.csv'
encoding_methods = 'GB2312'

# 1. 读取源表数据
source_data = pd.read_csv(source_path, encoding=encoding_methods)

# 2. 数据清洗和预处理
# 假设不需要清洗和预处理，源表数据已经干净

# 3. 创建生成表框架
# 直接利用源表进行生成

# 4. 数据分组和统计
# 统计上车人数
grouped_data = source_data.groupby(['班次', '上车站点序号']).size().reset_index(name='上车人数')
grouped_data = grouped_data.rename(columns={'上车站点序号': '站点序号'})
# 统计下车人数
down_grouped_data = source_data.groupby(['班次', '下车站点序号']).size().reset_index(name='下车人数')
down_grouped_data = down_grouped_data.rename(columns={'下车站点序号': '站点序号'})

# 合并两个表
merged_data = pd.merge(grouped_data, down_grouped_data,how='outer', on=['班次', '站点序号'], suffixes=('_上车', '_下车')).fillna(value=0)
# 浮点数化为整型
merged_data['上车人数'] = merged_data['上车人数'].fillna(0).astype(int)

merged_data['下车人数'] = merged_data['下车人数'].fillna(0).astype(int)

merged_data_sorted = merged_data.sort_values(by=['班次', '站点序号'])

# 计算客流量
merged_data_sorted['客流量']=merged_data_sorted['上车人数']-merged_data_sorted['下车人数']
# 对缺失值进行填充
merged_data.fillna(0, inplace=True)

# 输出生成表
print(merged_data_sorted)

# 将结果保存为CSV文件
merged_data_sorted.to_csv(destination_path, index=False, encoding=encoding_methods)
