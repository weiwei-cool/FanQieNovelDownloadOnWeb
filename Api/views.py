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

            async def fetch_and_print_book_info(books):
                semaphore = asyncio.Semaphore(4)  # 设置并发上限为4

                async def fetch_book_info(book):
                    async with semaphore:
                        await book.get_book_info()
                        book.parse_web_page()
                        book.parse_volume()
                        book.parse_images()

                tasks = [fetch_book_info(book) for book in books]
                await asyncio.gather(*tasks)

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


            cookie ='d_ticket=c9f70e3cfd4876b535774ee88cde10c17fef7; n_mh=L8EImyODpUyodNxeklHmUMo6M0js3ok1OIrDxDxJgo0; store-region=cn-yn; store-region-src=uid; ttwid=1%7CUVxAyif-zOYkFw2pD-mvcYx0veSKGH7djyXIcd8fNek%7C1697125965%7C14996b61c26d55c34b4ae8509749d6f5c8f20b442837f2b840edfd217a6033c7; _ga=GA1.1.407280117.1705663827; _ga_S37NWVC3ZR=GS1.1.1705672019.2.0.1705672019.0.0.0; passport_csrf_token=979e3f3c98f93a65bedb81975766588a; passport_csrf_token_default=979e3f3c98f93a65bedb81975766588a; odin_tt=9389b2d453db568445e6609699fd95706f14d945ccc324985bde6911747f2e83806f7b1135abffcfde660fe8f0252f9b; sid_guard=bee31f68cab2aa78145158f58e65fe36%7C1708103060%7C5184000%7CTue%2C+16-Apr-2024+17%3A04%3A20+GMT; uid_tt=1e58518f111b8f274229be2426c78211; uid_tt_ss=1e58518f111b8f274229be2426c78211; sid_tt=bee31f68cab2aa78145158f58e65fe36; sessionid=bee31f68cab2aa78145158f58e65fe36; sessionid_ss=bee31f68cab2aa78145158f58e65fe36; sid_ucp_v1=1.0.0-KDI4MmE2ODA4NzYyYTZhYmNjMjRkY2ZkOGVmNWJiODI4ZDhmOWJkNzkKHQiP5ra18wEQlKu-rgYYxxMgDDCDs5zMBTgCQPEHGgJobCIgYmVlMzFmNjhjYWIyYWE3ODE0NTE1OGY1OGU2NWZlMzY; ssid_ucp_v1=1.0.0-KDI4MmE2ODA4NzYyYTZhYmNjMjRkY2ZkOGVmNWJiODI4ZDhmOWJkNzkKHQiP5ra18wEQlKu-rgYYxxMgDDCDs5zMBTgCQPEHGgJobCIgYmVlMzFmNjhjYWIyYWE3ODE0NTE1OGY1OGU2NWZlMzY; novel_web_id=7279436395091871268; s_v_web_id=verify_ltx24m2v_js57O0rq_OIUV_4p0Q_8R2C_1oIFdGjBSD3U; Hm_lvt_2667d29c8e792e6fa9182c20a3013175=1711116384,1711171850,1711198527,1711260866; csrf_session_id=c80e62635e10b84d27d4720338826b48; Hm_lpvt_2667d29c8e792e6fa9182c20a3013175=1711373143; ttwid=1%7CUVxAyif-zOYkFw2pD-mvcYx0veSKGH7djyXIcd8fNek%7C1711373143%7Cf3de1158835605343ed6d4ad30bd8b448f9bb50073bdf3b48304a0257bc66c17; msToken=u5PngjKL83bK5z96pyIQ8DQ1zUoR8Oi7djyA0eX3pRkcicCIPcm5K_2GKi0CrrQdWCHSO9wxTRvTmwNe1HabQTdNsVE4wxzC8G0s21mJQqKEI_Gx-wLwLA=='

            books = [Book(parse_url(url), cookie) for url in urls]
            asyncio.run(fetch_and_print_book_info(books))
            [tools.logger.info(f'下载书籍:\n{book.__str__()}') for book in books]

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
