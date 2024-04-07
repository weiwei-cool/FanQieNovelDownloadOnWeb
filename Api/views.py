import asyncio
import os
import re
from urllib.parse import urlparse, parse_qs

import tools
from django.http import JsonResponse
from tools import Fanqie, DownloadNovel
from FanqieDecrypt import Book
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import History

# 下载的小说集合
download_object = []


@csrf_exempt  # 为了允许跨域请求，可选
@require_POST  # 确保只接受POST请求，可选
@tools.logger.catch  # 获取详细的报错信息
def download(request):  # 下载接口
    global download_object
    if request.method == 'POST':
        try:
            # 获取url数据
            tools.logger.info('正在获取url数据……')  # 打印日志
            data = json.loads(request.body.decode('utf-8'))
            urls = data.get('urls', [])
            # 初步去重
            urls = list(set(urls))
            tools.logger.info(f'已获取urls为:{urls}')

            # 获取下载方式
            format_ = data.get('format', 'txt')
            tools.logger.info(f'下载方式为{format_}')

            # 获取书本信息

            # async def fetch_and_print_book_info(books):
            #     semaphore = asyncio.Semaphore(4)  # 设置并发上限为4
            #
            #     async def fetch_book_info(book):
            #         async with semaphore:
            #             await book.get_book_info()
            #             book.parse_web_page()
            #             book.parse_volume()
            #             book.parse_images()
            #
            #     tasks = [fetch_book_info(book) for book in books]
            #     await asyncio.gather(*tasks)

            def fetch_and_print_book_info(books):

                for book in books:
                    book.get_book_info()
                    book.parse_web_page()
                    book.parse_volume()
                    book.parse_images()

            def parse_url(url: str) -> str:
                book_id = None
                u = urlparse(url)

                match u.netloc:  # 根据域名匹配
                    case "fanqienovel.com":  # Web 端
                        if u.path.startswith("/page/"):  # 书本详情页面
                            match = re.search(r'/page/(\d+)', url)
                            book_id = match.group(1)

                    case "changdunovel.com":  # App 分享链接
                        book_id = parse_qs(urlparse(url).query).get("book_id")[0]
                return book_id

            cookie = os.environ.get('COOKIE')
            tools.logger.info(f'使用cookie:{cookie}')

            books = [Book(parse_url(url), cookie) for url in urls]
            fetch_and_print_book_info(books)
            [tools.logger.info(f'下载书籍:\n{book.title}') for book in books]

            # 查看重复下载的书籍
            return_url = []

            # 开启下载进程
            for i in books:
                obid = f'{i.book_id}-{format_}'
                try:
                    history_ = History.objects.get(obid=obid)
                    if history_.obid == obid and format_ != 'epub':
                        tools.logger.warning(f'《{i.title}》重复提交！')
                        return_url.append(i.title)
                        continue
                    elif format_ == 'epub':
                        history_.delete()
                        b = History(book_id=i.book_id, obid=obid, file_name=f'{i.title}.{format_}', percent=0)
                        b.save()

                        d = DownloadNovel.DownloadNovel(i, format_)
                        download_object.append({'obid': obid, 'obj': d, 'book': i})
                        d.start()
                        tools.logger.info(f'《{i.title}》已开始下载')
                        continue
                except Exception as e:
                    tools.logger.info(f'《{i.title}》未重复, 已返回：{e}')

                b = History(book_id=i.book_id, obid=obid, file_name=f'{i.title}.{format_}', percent=0)
                b.save()

                d = DownloadNovel.DownloadNovel(i, format_)
                download_object.append({'obid': obid, 'obj': d, 'book': i})
                d.start()
                tools.logger.info(f'《{i.title}》已开始下载')

            # 返回成功和重复的数据
            response_data = {'message': 'Download request received', 'urls': urls, 'return': return_url}
            return JsonResponse(response_data, status=200)
        except Exception as e:
            tools.logger.error(f'发生异常: \n{e}')
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def download_del(_request, pk):  # 删除任务中的小说
    global download_object
    try:
        history_ = History.objects.filter(obid=pk)
        for j in history_:
            for i in download_object:
                if i['obid'] == pk:
                    i['obj'].stop()
                    tools.logger.info(f'《{i["book"].title}》已从下载列表中移除')
            j.delete()
        response_data = {'status': 'ok'}
        return JsonResponse(response_data, status=200)
    except Exception as e:
        tools.logger.error(f'错误！{e}')
        return JsonResponse({'status': 'error', 'error': str(e)}, status=400)


@csrf_exempt  # 为了允许跨域请求，可选
def history(_request):  # 查询所有正在任务中的小说
    records = History.objects.all()
    response_data = {'history': []}
    for record in records:
        tools.logger.info(f'查询正在任务中的小说：'
                          f'{record.file_name}(obid: {record.obid}) 已下载 {record.percent}%')
        response_data['history'].append({'book_id': record.book_id,
                                         'obid': record.obid,
                                         'file_name': record.file_name,
                                         'percent': record.percent})
    response_data['history'] = response_data['history'][::-1]
    return JsonResponse(response_data, status=200)


def history_id(_request, pk):  # 根据具体obid查询小说下载数据
    history_entry = History.objects.get(obid=pk)
    tools.logger.info(f'查询正在任务中的小说：'
                      f'{history_entry.file_name}(obid: {history_entry.obid}) 已下载 {history_entry.percent}%')
    return JsonResponse({'percent': history_entry.percent}, status=200)


def get_config(_request):  # 获取信息
    # 公开下载链接
    public_url = os.environ.get('PUBLIC_URL')

    # 默认下载模式
    default_download_mode = os.environ.get('DEFAULT_DMODE')
    if not default_download_mode:
        default_download_mode = 'epub'

    ret = {
        'download_url': public_url,
        'default_download_mode': default_download_mode,
        'version': tools.version
    }
    return JsonResponse(ret, status=200)
