## 一、项目介绍

1.概述

前端共包含有两个网页，第一个网页整体结构已经搭建完毕，第二个网页还有部分功能没有实现。

预期图分别如下：

![1](D:\pythonProject\Sleep\docs\1.jpg)

![2](D:\pythonProject\Sleep\docs\2.jpg)

2.实现方法

前端网页采用flask+echarts实现

后端服务器采用mysql+flask搭建，目前简单实现了前后端通信功能以及后端与数据库之间连接的建立



## 二、环境搭建

使用命令行模式切换到Sleep目录下，然后输入以下命令即可完成环境配置

```
conda create -n sleep python==3.9
pip install -r requirements
```

启动第一个网页

```
python main.py
```

启动第二个网页：

双击sleep/sleep2/templates/index.html即可（因为目前还没有与后端衔接，所以不用运行python程序）

