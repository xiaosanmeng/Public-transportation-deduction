# -*- coding: utf-8 -*-
import pandas as pd
################################
# 需要下载包pandas配置到解释器环境之中 #
# 源路径需要csv数据 #
# 数据编码方式采用GB2312，便于使用Excel打开 #
################################


source_path = 'source_data.csv'
destination_path = 'max_min_time_result.csv'
encoding_methods = 'GB2312'

# 1. 读取源表数据
source_data = pd.read_csv(source_path, encoding=encoding_methods)

# 2. 数据清洗和预处理
# 假设不需要清洗和预处理，源表数据已经干净

# 3. 创建生成表框架
# 直接利用源表进行生成

# 4. 数据分组和统计
# 4.1统计上车人数
grouped_data = source_data.groupby(['班次', '上车站点序号']).size().reset_index(name='上车人数')
grouped_data = grouped_data.rename(columns={'上车站点序号': '站点序号'})
# 统计下车人数
down_grouped_data = source_data.groupby(['班次', '下车站点序号']).size().reset_index(name='下车人数')
down_grouped_data = down_grouped_data.rename(columns={'下车站点序号': '站点序号'})

# 4.2合并两个表
merged_data = pd.merge(grouped_data, down_grouped_data,how='outer', on=['班次', '站点序号'], suffixes=('_上车', '_下车')).fillna(value=0)
# 浮点数化为整型
merged_data['上车人数'] = merged_data['上车人数'].fillna(0).astype(int)

merged_data['下车人数'] = merged_data['下车人数'].fillna(0).astype(int)

merged_data_sorted = merged_data.sort_values(by=['班次', '站点序号'])

# 4.3计算客流量
merged_data_sorted['客流量']=merged_data_sorted['上车人数']-merged_data_sorted['下车人数']

# 4.4计算每个站点首个乘客刷卡时刻和最后一个乘客的刷卡时刻

# 对每个班次和站点序号进行分组，分别求取上车时间的最小值和下车时间的最小值，并将两者合并
min_data_1 = source_data.groupby(['班次', '上车站点序号']).agg({'上车时间': 'min'}).reset_index()
min_data_1 = min_data_1.rename(columns={'上车站点序号': '站点序号','上车时间':'首个刷卡时间'})
min_data_2 = source_data.groupby(['班次', '下车站点序号']).agg({'下车时间': 'min'}).reset_index()
min_data_2 = min_data_2.rename(columns={'下车站点序号': '站点序号','下车时间':'首个刷卡时间'})
min_data = pd.merge(min_data_1, min_data_2, how='outer', on=['班次', '站点序号','首个刷卡时间'])

# 与上一步类似，这次求取的是最大值
max_data_1 = source_data.groupby(['班次', '上车站点序号']).agg({'上车时间': 'max'}).reset_index()
max_data_1 = max_data_1.rename(columns={'上车站点序号': '站点序号','上车时间':'最后一个刷卡时间'})
max_data_2 = source_data.groupby(['班次', '下车站点序号']).agg({'下车时间': 'max'}).reset_index()
max_data_2 = max_data_2.rename(columns={'下车站点序号': '站点序号','下车时间':'最后一个刷卡时间'})
max_data = pd.merge(max_data_1,max_data_2,how='outer',on=['班次', '站点序号','最后一个刷卡时间'])

# 将结果合并到原始数据中
result = pd.merge(merged_data_sorted, min_data, how='outer', on=['班次', '站点序号'], suffixes=('', '_第一个'))
result = pd.merge(result, max_data, how='outer', on=['班次', '站点序号'], suffixes=('', '_最后一个'))

# 对缺失值进行填充
merged_data.fillna(0, inplace=True)
# print(result)
result.to_csv(destination_path, index=False, encoding=encoding_methods)

