# Pandas库详细解释

# Python Pandas 库详解

## 1. Pandas 是什么以及主要用途

**Pandas** 是一个开源的 Python 数据分析库，提供了高性能、易用的数据结构和数据分析工具。名称 "Pandas" 源自 "Panel Data"（面板数据）的缩写。

**主要用途**：
- 数据清洗和处理
- 数据分析和探索
- 数据可视化（通常与 Matplotlib/Seaborn 结合）
- 时间序列分析
- 数据预处理和特征工程
- 从各种文件格式读取和写入数据

## 2. 核心数据结构

### Series（系列）
一维标签数组，类似于带标签的列表或字典

```python
import pandas as pd
import numpy as np

# 创建 Series
s = pd.Series([1, 3, 5, np.nan, 6, 8])
print(s)

# 带自定义索引的 Series
s2 = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print(s2)

# 从字典创建 Series
data = {'a': 1, 'b': 2, 'c': 3}
s3 = pd.Series(data)
print(s3)
```

### DataFrame（数据框）
二维标签数据结构，类似于电子表格或 SQL 表

```python
# 创建 DataFrame
data = {
    '姓名': ['张三', '李四', '王五', '赵六'],
    '年龄': [25, 30, 35, 28],
    '城市': ['北京', '上海', '广州', '深圳'],
    '工资': [50000, 60000, 70000, 55000]
}
df = pd.DataFrame(data)
print(df)

# 查看 DataFrame 的基本信息
print("数据形状:", df.shape)
print("列名:", df.columns)
print("索引:", df.index)
print("数据类型:\n", df.dtypes)
```

## 3. 常用的数据操作功能

### 读取数据
```python
# 从 CSV 文件读取
df = pd.read_csv('data.csv')

# 从 Excel 文件读取
df = pd.read_excel('data.xlsx')

# 从 JSON 文件读取
df = pd.read_json('data.json')

# 从 SQL 数据库读取
import sqlite3
conn = sqlite3.connect('database.db')
df = pd.read_sql_query('SELECT * FROM table_name', conn)
```

### 数据清洗
```python
# 处理缺失值
df = pd.DataFrame({
    'A': [1, 2, np.nan, 4],
    'B': [5, np.nan, np.nan, 8],
    'C': [10, 11, 12, 13]
})

# 检查缺失值
print("缺失值统计:\n", df.isnull().sum())

# 填充缺失值
df_filled = df.fillna({'A': df['A'].mean(), 'B': 0})
print("填充后的数据:\n", df_filled)

# 删除缺失值
df_dropped = df.dropna()
print("删除缺失值后的数据:\n", df_dropped)

# 处理重复值
df_duplicates = pd.DataFrame({
    'A': [1, 2, 2, 3, 4],
    'B': [5, 6, 6, 7, 8]
})
df_no_duplicates = df_duplicates.drop_duplicates()
print("去重后的数据:\n", df_no_duplicates)
```

### 数据筛选
```python
# 创建示例数据
df = pd.DataFrame({
    '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
    '年龄': [25, 30, 35, 28, 32],
    '部门': ['技术', '销售', '技术', '市场', '销售'],
    '工资': [50000, 60000, 70000, 55000, 65000]
})

# 条件筛选
tech_employees = df[df['部门'] == '技术']
print("技术部门员工:\n", tech_employees)

# 多条件筛选
high_salary_tech = df[(df['部门'] == '技术') & (df['工资'] > 55000)]
print("高薪技术员工:\n", high_salary_tech)

# 使用 query 方法
result = df.query('年龄 > 30 and 工资 > 60000')
print("30岁以上且工资高于60000的员工:\n", result)

# 选择特定列
selected_columns = df[['姓名', '工资']]
print("选择的列:\n", selected_columns)

# 使用 loc 和 iloc
# loc 基于标签选择
print("前两行:\n", df.loc[0:1])

# iloc 基于位置选择
print("前两行:\n", df.iloc[0:2])
```

### 分组聚合
```python
# 按部门分组并计算平均工资
grouped = df.groupby('部门')['工资'].mean()
print("各部门平均工资:\n", grouped)

# 多个聚合函数
agg_result = df.groupby('部门').agg({
    '工资': ['mean', 'min', 'max', 'count'],
    '年龄': 'mean'
})
print("多维度聚合:\n", agg_result)

# 按多个列分组
multi_group = df.groupby(['部门', '年龄']).size()
print("多列分组:\n", multi_group)
```

## 4. 常用的函数和方法

### 数据查看和统计
```python
# 查看前几行
print(df.head(2))

# 查看后几行
print(df.tail(2))

# 描述性统计
print(df.describe())

# 相关性分析
print(df.corr())
```

### 数据排序
```python
# 按工资降序排序
sorted_df = df.sort_values('工资', ascending=False)
print("按工资排序:\n", sorted_df)

# 按多列排序
multi_sorted = df.sort_values(['部门', '工资'], ascending=[True, False])
print("多列排序:\n", multi_sorted)
```

### 数据转换
```python
# 添加新列
df['年薪'] = df['工资'] * 12
print("添加年薪列:\n", df)

# 应用函数
df['年龄组'] = df['年龄'].apply(lambda x: '青年' if x < 30 else '中年')
print("添加年龄组:\n", df)

# 重命名列
df_renamed = df.rename(columns={'姓名': 'name', '年龄': 'age'})
print("重命名列:\n", df_renamed)

# 数据透视表
pivot_table = pd.pivot_table(df, values='工资', index='部门', 
                            aggfunc='mean')
print("数据透视表:\n", pivot_table)
```

## 5. 实际应用场景和示例

### 场景1：销售数据分析
```python
# 创建销售数据示例
sales_data = {
    '日期': pd.date_range('2023-01-01', periods=100, freq='D'),
    '产品': np.random.choice(['A', 'B', 'C'], 100),
    '销售额': np.random.randint(100, 1000, 100),
    '地区': np.random.choice(['东区', '西区', '南区', '北区'], 100)
}
sales_df = pd.DataFrame(sales_data)

# 分析每个产品的总销售额
product_sales = sales_df.groupby('产品')['销售额'].sum()
print("产品销售额:\n", product_sales)

# 分析每个地区的月销售额
sales_df['月份'] = sales_df['日期'].dt.month
region_monthly_sales = sales_df.groupby(['地区', '月份'])['销售额'].sum().unstack()
print("地区月销售额:\n", region_monthly_sales)

# 找出销售额最高的日期
top_sales_day = sales_df.loc[sales_df['销售额'].idxmax()]
print("销售额最高的一天:\n", top_sales_day)
```

### 场景2：学生成绩分析
```python
# 创建学生成绩数据
np.random.seed(42)
students = {
    '学号': range(1, 101),
    '班级': np.random.choice(['一班', '二班', '三班'], 100),
    '数学': np.random.randint(60, 100, 100),
    '语文': np.random.randint(60, 100, 100),
    '英语': np.random.randint(60, 100, 100)
}
student_df = pd.DataFrame(students)

# 计算总分和平均分
student_df['总分'] = student_df[['数学', '语文', '英语']].sum(axis=1)
student_df['平均分'] = student_df[['数学', '语文', '英语']].mean(axis=1)

# 分析各班平均成绩
class_avg = student_df.groupby('班级')[['数学', '语文', '英语', '平均分']].mean()
print("各班平均成绩:\n