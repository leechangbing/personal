import pandas as pd


# 测试series
def test_series():
    s = pd.Series([1,2,3,4,5,6], index=['a','b','c','d','e','f'])
    print(s)


# 描述功能
def test_dataframe_info():
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['NY', 'LA', 'Chicago']
    })
    print(df)

    print(df.head())
    print(df.tail())
    print(df.info())
    print(df.describe())
    print(df.shape)
    print(df.columns)


# 索引功能
def test_dataframe_idx():
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['NY', 'LA', 'Chicago']
    })

    print(df['Name'])
    print(df[['Name', 'Age']])
    print(df.iloc[0])
    print(df.iloc[0,0])
    print(df.iloc[0:21])


# 填充功能
def test_dataframe_fillna():
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['NY', 'LA', 'Chicago']
    })

    df.fillna({'Age': 25}, inplace=True)
    print(df)


# 排序功能
def test_dataframe_sort():
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['NY', 'LA', 'Chicago']
    })

    df = df.sort_values(by=['Age'], ascending=False)
    print(df)


# 排序功能
def test_dataframe_group():
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['NY', 'LA', 'Chicago']
    })

    print(df.groupby('Age'))


# 新增&删除功能
def test_dataframe_add_delete():
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['NY', 'LA', 'Chicago']
    })

    df['Gender'] = ['Male', 'Female', 'Female']
    print(df)

    df.drop(['Age'], axis=1, inplace=True)
    print(df)


# 拼接与连接功能
def test_dataframe_concat_merge():
    df1 = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['NY', 'LA', 'Chicago']
    })

    df2 = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['NY', 'LA', 'Chicago']
    })

    print(pd.concat([df1,df2]))
    print(pd.merge(df1,df2,on='Name'))



def test_dataframe_apply():
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['NY', 'LA', 'Chicago']
    })

    df['new_Age'] = df['Age'].apply(lambda x: x+1)
    print(df)


if __name__ == '__main__':
    print(pd.__version__)

    test_series() # 测试series

    test_dataframe_info() # 测试datafrome信息

    test_dataframe_idx() # 测试索引功能

    test_dataframe_fillna() # 测试填充功能

    test_dataframe_sort() # 测试排序功能

    test_dataframe_group() # 测试分组功能

    test_dataframe_add_delete() # 测试新增&删除功能

    test_dataframe_concat_merge() # 测试拼接与连接功能

    test_dataframe_apply() # 测试应用函数
