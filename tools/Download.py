import os
import tools
from webdav4.client import Client
import threading

from Api.models import History, BookInfo
from FanqieDecrypt import Book


class Download(threading.Thread):

    def __init__(self, book_info: GetBookInfo):
        self.mode = mode
        self.book_id = book_id
        self.obid = f'{self.book_id}-{self.mode}'

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
        tools.logger.info(f'开始下载小说: \n{self.fanqie.__str__()}')


class GetBookInfoThreading(threading.Thread):
    def __init__(self, book_id, mode):
        self.book = None
        self.mode = mode
        self.book_id = book_id
        self.obid = f'{self.book_id}-{self.mode}'

        # 停止子进程
        self._stop_flag = False
        self._stop_event = threading.Event()

        super().__init__()

    def run(self) -> None:
        cookie = os.environ.get('COOKIE')
        self.book = Book(self.book_id, cookie)
