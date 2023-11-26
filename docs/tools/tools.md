# Tools模块

## 文件列表

- \__init__.py
- DownloadNovel.py
- Fanqie.py

## 介绍

### 根模块(__init__.py)

根模块是一个底层的处理工具。  
您需要使用根模块中的`logger`进行日志记录。  
该类包含了一系列方法，用于获取小说的基本信息、规范化文件名以及修复出版物文本。通过这些方法，FanqieNovel类提供了方便而强大的功能，使得处理小说数据变得更加简便和可靠。

### DownloadNovel.py
DownloadNovel类是一个用于下载小说的线程类，通过传入[Fanqie](#fanqiepy)对象实例化。  
该类提供了下载小说的功能，支持两种下载模式：'txt'和'epub'。通过线程的方式运行下载操作，确保在下载过程中不阻塞主线程。

### Fanqie.py
FanqieNovel类是一个用于获取小说基本信息和目录的对象。  
通过传入小说目录链接和下载方式，该类可以实例化一个FanqieNovel对象，从而提供了获取小说相关信息的功能。