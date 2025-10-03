# isbn_search

本项目基于python3，实现通过书籍的isbn码查询书籍信息的功能。

项目链接：[https://github.com/vistar-terry/isbn_search](https://github.com/vistar-terry/isbn_search)

相关博客链接：[Python爬虫实现isbn查询豆瓣书籍详细信息](https://blog.csdn.net/maizousidemao/article/details/102532075)

如有疑问，欢迎提 [issues](https://github.com/vistar-terry/isbn_search/issues) ，或在博客评论区留言。



### 一、目录说明

1. book.py：脚本文件
2. requirements.txt：依赖环境版本



### 二、使用说明

#### 1. 安装环境

在项目根目录执行以下命令，安装项目所需环境：

```bash
pip install -r requirements.txt
```



#### 2. 快速测试

在 `book.py` 同级目录执行以下命令：

```bash
python book.py 9787121369421
```

输出如下：

![image-20230503215055017](img/image-20230503215055017.png)



### 三、更新日志

-   2019年9月28日：通过isbn ID 搜索图书信息
-   2020年3月30日：添加headers伪装真实浏览器
-   2023年3月3日：
    -   将PhantomJS浏览器驱动打包到仓库
    -   添加评价人数
-   2025年10月1日：
    -   豆瓣网页结构改变，修改爬虫搜索逻辑，使用subject_id
    -   使用 requests 库替代 PhantomJS 浏览器获取网页信息



### 四、TO DO

1. 优化查询效率



### 五、交流讨论

![git](img/git.png)
