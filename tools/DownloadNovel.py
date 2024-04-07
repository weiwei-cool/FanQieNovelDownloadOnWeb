import asyncio
import re
import os
import time

from FanqieDecrypt import Book

import tools
import yaml
import threading
import requests
from urllib.parse import urljoin
from webdav4.client import Client
from . import Fanqie
from ebooklib import epub
from Api.models import History
from pathlib import Path


class DownloadNovel(threading.Thread):
    """
    下载小说，应传入番茄对象
    """

    def __init__(self, book: Book, mode):
        # 番茄小说对象
        self.mode = mode
        self.book: Book = book
        self.obid = f'{self.book.book_id}-{self.mode}'
        # 停止子进程
        self._stop_flag = False
        self._stop_event = threading.Event()

        # 自定义WebDav路径
        self.is_webdav = os.environ.get('IS_WEBDAV')
        if self.is_webdav:
            self.webdav_username = os.environ.get('WEBDAV_USERNAME')
            self.webdav_pwd = os.environ.get('WEBDAV_PWD')
            self.webdav_url = os.environ.get('WEBDAV_URL')
            self.webdav = Client(base_url=self.webdav_url,
                                 auth=(self.webdav_username, self.webdav_pwd))
            tools.logger.info(f'已成功加载webdav服务器({self.webdav_url})')

        # 自定义保存路径
        self.custom_path = os.environ.get('CUSTOM_PATH')
        if not self.custom_path:
            self.custom_path = './books'
            os.makedirs(self.custom_path, exist_ok=True)
            tools.logger.warning(f'您未设置自定义保存路径，将使用默认路径: {self.custom_path}')

        super().__init__()

    def run(self) -> None:
        # 数据库中获取小说对象
        history_entry = History.objects.get(obid=self.obid)
        tools.logger.info(f'开始下载小说: \n{self.book.title}')

        # 判断下载模式
        if self.mode == 'txt':
            tools.logger.info(f'正在以txt模式下载小说')

            content = f"""{self.book.title}
            {self.book.intro}
            """
            # 获取所有章节链接
            start_index = 0

            file_name = self.book.title + ".txt"
            file_path = os.path.join(self.custom_path, file_name)

            # 获取章节数
            chapter_num = self.book.chapter_num
            chapter_num_now = 0

            try:
                # 遍历每个章节链接
                for chapter in self.book.volumes_object[start_index:]:
                    pass
                # 根据编码转换小说内容字符串为二进制数据
                data = content.encode('utf-8', errors='ignore')

                # 保存文件
                with open(file_path, "wb") as f:
                    f.write(data)

                file_path = os.path.join(self.custom_path, file_name)
                file_path = Path(file_path)
                if self.is_webdav:
                    self.webdav.upload_file(from_path=file_path,
                                            to_path=os.path.join('/public', file_name),
                                            overwrite=True)
                    tools.logger.info(f'《{self.book.title}》已成功上传webdav服务器')

                # 打印完成信息
                tools.logger.info(f'已保存{self.book.title}.txt至本地')

            except BaseException as e:
                # 捕获所有异常，及时保存文件
                tools.logger.error(f'发生异常: \n{e}')
                tools.logger.info('正在尝试保存文件')
                # 根据编码转换小说内容字符串为二进制数据
                data = content.encode('utf-8', errors='ignore')

                # 保存文件
                file_path = os.path.join(self.custom_path, file_name)
                with open(file_path, "wb") as f:
                    f.write(data)

                tools.logger.info('文件已保存！')
                return

        elif self.mode == 'epub':
            # 拼接文件名和文件路径
            file_name = self.book.title + ".epub"
            file_path = os.path.join(self.custom_path, file_name)

            updata_mode = False

            book_o = None
            try:
                book_o = epub.read_epub(file_path, {'ignore_ncx': True})
                # yaml_item = book_o.get_item_with_id('yaml')
                # yaml_content = yaml_item.get_content().decode('utf-8')
                # book_id = yaml.safe_load(yaml_content)['fqid']
            except Exception as e:
                tools.logger.error(e)
            else:
                updata_mode = True

            tools.logger.info(f'正在以epub模式下载小说')

            # 创建epub电子书
            book = epub.EpubBook()

            # 下载封面
            self.book.parse_images()
            self.book.get_image()

            # 创建一个封面图片
            book.set_cover("image.jpg", self.book.image)

            # 设置书的元数据
            book.set_title(self.book.title)
            book.set_language('zh-CN')
            book.add_author(self.book.author_name)
            book.add_metadata('DC', 'description', self.book.intro)

            yaml_data = {
                'fqid': self.obid
            }
            yaml_content = yaml.dump(yaml_data)

            # 设置 fqid 元数据
            yaml_item = epub.EpubItem(uid='yaml', file_name='metadata.yaml', media_type='application/octet-stream',
                                      content=yaml_content)
            book.add_item(yaml_item)

            # intro chapter
            intro_e = epub.EpubHtml(title='Introduction', file_name='intro.xhtml', lang='hr')
            intro_e.content = (f'<html><head></head><body>'
                               f'<img src="image.jpg" alt="Cover Image"/>'
                               f'<h1>{self.book.title}</h1>'
                               f'<p>{self.book.intro}</p>'
                               f'</body></html>')
            book.add_item(intro_e)

            # 创建索引
            book.toc = (epub.Link('intro.xhtml', '简介', 'intro'),)
            book.spine = ['nav', intro_e]

            try:
                def get_text(_stop_event, book: Book, sleep: int, history_entry: History, updata_mode, book_o):
                    chapter_num_now = 0
                    for volume in book:
                        volume.parse_chapter()
                        for chapter in volume:
                            if updata_mode:
                                context = book_o.get_item_with_href(f'chapter_'
                                                                    f'{volume.volume_id}_'
                                                                    f'{chapter.chapter_id_index}.xhtml')
                                if context is not None:
                                    # 提取文章标签中的文本
                                    chapter_content = re.search(r"<body>([\s\S]*?)</body>",
                                                                context.get_content().decode()).group(1)
                                    chapter.html_content = re.sub(r'<h2.*?>.*?</h2>', '', chapter_content)

                                    chapter_num_now += 1
                                    history_entry.percent = round(
                                        (chapter_num_now / book.chapter_num) * 100, 2)
                                    history_entry.save()

                                    tools.logger.info(
                                        f'已从本地获取 {chapter.chapter_title}, 进度：{history_entry.percent}%')

                                    continue

                            time.sleep(sleep)
                            if _stop_event.is_set():
                                break
                            chapter.get_html_content()
                            chapter.parse_content()
                            chapter.decrypt_content()

                            chapter_num_now += 1
                            history_entry.percent = round(
                                (chapter_num_now / book.chapter_num) * 100, 2)
                            history_entry.save()

                            # 打印进度信息
                            tools.logger.info(f'已获取 {chapter.chapter_title}, 进度：{history_entry.percent}%')

                # loop = asyncio.new_event_loop()
                # asyncio.set_event_loop(loop)
                # loop.run_until_complete(get_text(self._stop_event,
                #                                  self.book, 0.25,
                #                                  history_entry, updata_mode, book_o))
                # loop.close()

                tools.logger.info(self.book.chapter_num)

                get_text(self._stop_event, self.book, 0.25,
                         history_entry, updata_mode, book_o)

                # 遍历每个卷
                for volume in self.book:
                    first_chapter = None
                    # 定义目录索引
                    toc_index = ()

                    # 遍历每个章节链接
                    for chapter in volume:
                        # 在小说内容字符串中添加章节标题和内容
                        text = epub.EpubHtml(title=chapter.chapter_title,
                                             file_name=f'chapter_{volume.volume_id}_{chapter.chapter_id_index}.xhtml')
                        text.content = (f'<h2>{chapter.chapter_title}</h2>'
                                        f'{chapter.html_content}')

                        toc_index = toc_index + (text,)
                        book.spine.append(text)

                        # 寻找第一章
                        if chapter.chapter_id_index == 1:
                            first_chapter = f'chapter_{volume.volume_id}_{chapter.chapter_id_index}.xhtml'

                        # 加入epub
                        book.add_item(text)

                    # 加入书籍索引
                    book.toc = book.toc + ((epub.Section(volume.volume_title, href=first_chapter),
                                            toc_index,),)
            # 捕获异常
            except BaseException as e:
                # 捕获所有异常
                tools.logger.error(f'发生异常: \n{e}')
                return

            # 添加 navigation 文件
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())

            # 书写电子书
            epub.write_epub(file_path, book, {})

            # webdav上传
            file_path = Path(file_path)
            if self.is_webdav:
                self.webdav.upload_file(from_path=file_path,
                                        to_path=os.path.join('/public', file_name),
                                        overwrite=True)
                tools.logger.info(f'《{self.book.title}》已成功上传webdav服务器')

            tools.logger.info(f'已保存{self.book.title}.epub至本地')

    # 停止子进程函数
    def stop(self):
        self._stop_event.set()
