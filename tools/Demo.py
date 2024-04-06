from FanqieDecrypt.Book import Book
import asyncio

cookie = 'd_ticket=c9f70e3cfd4876b535774ee88cde10c17fef7; n_mh=L8EImyODpUyodNxeklHmUMo6M0js3ok1OIrDxDxJgo0; store-region=cn-yn; store-region-src=uid; ttwid=1%7CUVxAyif-zOYkFw2pD-mvcYx0veSKGH7djyXIcd8fNek%7C1697125965%7C14996b61c26d55c34b4ae8509749d6f5c8f20b442837f2b840edfd217a6033c7; _ga=GA1.1.407280117.1705663827; _ga_S37NWVC3ZR=GS1.1.1705672019.2.0.1705672019.0.0.0; passport_csrf_token=979e3f3c98f93a65bedb81975766588a; passport_csrf_token_default=979e3f3c98f93a65bedb81975766588a; odin_tt=9389b2d453db568445e6609699fd95706f14d945ccc324985bde6911747f2e83806f7b1135abffcfde660fe8f0252f9b; sid_guard=bee31f68cab2aa78145158f58e65fe36%7C1708103060%7C5184000%7CTue%2C+16-Apr-2024+17%3A04%3A20+GMT; uid_tt=1e58518f111b8f274229be2426c78211; uid_tt_ss=1e58518f111b8f274229be2426c78211; sid_tt=bee31f68cab2aa78145158f58e65fe36; sessionid=bee31f68cab2aa78145158f58e65fe36; sessionid_ss=bee31f68cab2aa78145158f58e65fe36; sid_ucp_v1=1.0.0-KDI4MmE2ODA4NzYyYTZhYmNjMjRkY2ZkOGVmNWJiODI4ZDhmOWJkNzkKHQiP5ra18wEQlKu-rgYYxxMgDDCDs5zMBTgCQPEHGgJobCIgYmVlMzFmNjhjYWIyYWE3ODE0NTE1OGY1OGU2NWZlMzY; ssid_ucp_v1=1.0.0-KDI4MmE2ODA4NzYyYTZhYmNjMjRkY2ZkOGVmNWJiODI4ZDhmOWJkNzkKHQiP5ra18wEQlKu-rgYYxxMgDDCDs5zMBTgCQPEHGgJobCIgYmVlMzFmNjhjYWIyYWE3ODE0NTE1OGY1OGU2NWZlMzY; novel_web_id=7279436395091871268; s_v_web_id=verify_ltx24m2v_js57O0rq_OIUV_4p0Q_8R2C_1oIFdGjBSD3U; Hm_lvt_2667d29c8e792e6fa9182c20a3013175=1711116384,1711171850,1711198527,1711260866; csrf_session_id=c80e62635e10b84d27d4720338826b48; Hm_lpvt_2667d29c8e792e6fa9182c20a3013175=1711373143; ttwid=1%7CUVxAyif-zOYkFw2pD-mvcYx0veSKGH7djyXIcd8fNek%7C1711373143%7Cf3de1158835605343ed6d4ad30bd8b448f9bb50073bdf3b48304a0257bc66c17; msToken=u5PngjKL83bK5z96pyIQ8DQ1zUoR8Oi7djyA0eX3pRkcicCIPcm5K_2GKi0CrrQdWCHSO9wxTRvTmwNe1HabQTdNsVE4wxzC8G0s21mJQqKEI_Gx-wLwLA=='

book_id = 7077757205910391838

book = Book(book_id, cookie)


async def get(book: object, sleep: int = 0):
    await book.get_book_info()

    book.parse_web_page()
    book.parse_volume()

    for volume in book:
        volume.parse_chapter()
        for chapter in volume:
            await chapter.get_html_content()
            chapter.parse_content()
            chapter.decrypt_content()
            await asyncio.sleep(sleep)

asyncio.run(get(book))

for volume in book:
    print(volume.volume_title)
    for chapter in volume:
        print(chapter.html_content)
