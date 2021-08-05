# 逻辑回归训练

### 关于数据整理
准备好数据样本 sample/sample2.xlsx  
数据将按照 sample/数据处理方式.txt 来预处理，并生成 out/logistic/sample2.csv, sample2_titles.txt, sample2_data_mapping.txt 三个文件
其中 sample2_data_mapping.txt 文件里面有具体的每个数据的重新编号，如 少儿部 -> 1 等类似的编号。

#### 数据整理   
```python handle_data2.py```

#### 数据训练
```python main.py```   

输出结果保存在 out/logistic/result.txt 文件

   