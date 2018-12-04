import json
import requests
import re
import time


def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>'
                         +'(.*?)</p>.*?score.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>', re.S)#正则匹配

    items = re.findall(pattern, html)#根据正则表达式进行查找
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5].strip() + item[6].strip(),
            }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as file:
        print(type(json.dumps(content)))
        file.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        print(type(item))
        write_to_file(item)


if __name__ == '__main__':
    for i in range(3):
        main(offset=i * 10)
        time.sleep(1)


'''

<a href="/films/1203" title="霸王别姬" data-act="boarditem-click" data-val="{movieId:1203}">霸王别姬</a>
<p class="star">
                主演：张国荣,张丰毅,巩俐
        </p>
        
<p class="score"><i class="integer">9.</i><i class="fraction">6</i></p>

<dd>
                        <i class="board-index board-index-1">1</i>
    <a href="/films/1203" title="霸王别姬" class="image-link" data-act="boarditem-click" data-val="{movieId:1203}">
      <img src="//ms0.meituan.net/mywww/image/loading_2.e3d934bf.png" alt="" class="poster-default" />
      <img data-src="https://p1.meituan.net/movie/20803f59291c47e1e116c11963ce019e68711.jpg@160w_220h_1e_1c" alt="霸王别姬" class="board-img" />
    </a>
    <div class="board-item-main">
      <div class="board-item-content">
              <div class="movie-item-info">
        <p class="name"><a href="/films/1203" title="霸王别姬" data-act="boarditem-click" data-val="{movieId:1203}">霸王别姬</a></p>
        <p class="star">
                主演：张国荣,张丰毅,巩俐
        </p>
<p class="releasetime">上映时间：1993-01-01</p>    </div>
    <div class="movie-item-number score-num">
<p class="score"><i class="integer">9.</i><i class="fraction">6</i></p>        
    </div>

      </div>
    </div>

                </dd>


'''

