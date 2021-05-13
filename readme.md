# 逻辑回归训练

### 数据整理
准备好数据样本 sample.xlsx  
自动识别【标题】中特殊字符并处理  
1. **去掉** (不作为训练数据)
2. **只需数字** (获取数字部分作为训练数据)
3. **虚拟** (将按照sample数据的总类，自动添加列类别，如 学校（小学，中学，大学），则自动添加列 学校小学，学校中学),不添加大学，因为互斥，不是小学、中学的话，就是大学。
4. **枚举** (将按照sample数据的总类，自动编号，如 学校（小学，中学，大学），小学==0， 中学==1， 大学==2，具体数据查看 out/type_enum.txt)
5. **年月日** (将日期创建成年、月、日三个列类别, 如 开学时间, 2020/09/05， 则自动添加 开学时间年、开学时间月、开学时间日)

运行数据整理脚本   
```python handle_data.py```

运行训练脚本
```python main.py```

### python环境准备
```pip install sklearn```  
```...```  
```pip install openpyxl```
   
   
### 1000条样例数据训练结果  
score Scikit learn:  0.7801047120418848
