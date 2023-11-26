# __init__.py
根模块是一个底层的处理工具。  
## logger
该项目使用来自loguru的logger。  
调用方法：（logger的详细方法请自行百度）
```python
import tools
tools.logger.info('print')
```
## rename
该函数属于静态底层函数，用以格式化小说命名中可能使程序出错的非法名称
调用方法：
```python
import tools
tools.rename(
    name= ""  #传入需要格式化的字符
)
```
|  参数  | 类型  | 是否必填 |
|:----:|:---:|:----:|
| name | str |  是   |

## fix_publisher
该函数为补丁函数，用以修补当下载的小说为`出版物`时遗留的xml标签。  
调用方法：
```python
import tools
tools.fix_publisher(
    text= ""  #传入需要修补的文本
)
```
|  参数  | 类型  | 是否必填 |
|:----:|:---:|:----:|
| text | str |  是   |
[cinwell website](../logo.png ':include :type=iframe width=100% height=400px')
