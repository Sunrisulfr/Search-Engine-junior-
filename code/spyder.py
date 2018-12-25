import xml.etree.ElementTree as ET
import requests
import json

def save_data(title, id, body, url, doc_dir_path='../data/news/'):
    if '//' in body:
        body = body[:body.index('//')]
    body = body.replace(" ", "")
    doc = ET.Element("doc")
    ET.SubElement(doc, "id").text = "%d" % (id)
    ET.SubElement(doc, "url").text = "https://www.toutiao.com" + url
    ET.SubElement(doc, "title").text = title
    ET.SubElement(doc, "body").text = body
    tree = ET.ElementTree(doc)
    tree.write(doc_dir_path + "%d.xml" % (id), encoding='utf-8', xml_declaration=True)

def get_data(param, root_url, headers, num=100):
    params = param
    i = 1
    urls = []
    while True:
        if i > num : break
        wbdata = requests.get(root_url, headers=headers, params=params).text
        data = json.loads(wbdata)
        news = data['data']
        for n in news:
            try:
                title = n['title']
                abstract = n['abstract']
                url = n['source_url']
                if url not in urls:
                    urls.append(url)
                    print(title, '\n', abstract, '\n')
                    save_data(title, i, abstract, url)
                    i = i + 1
                    if i > num : break
            except KeyError:
                continue
        next_num = data['next']['max_behot_time']
        params['max_behot_time'] = next_num


if __name__ == '__main__':
    root_url = 'https://www.toutiao.com/api/pc/feed/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        ,
        'cookie': 'WEATHER_CITY=%E5%8C%97%E4%BA%AC; uuid="w:50ca0b9cdd5940d4af7d5685455f50b1"; csrftoken=d66f7de14b4144ac445bf973380393a6; tt_webid=6614072048120350212; tt_webid=6614072048120350212; UM_distinctid=166f0b27b0c333-0a73cb4cb911ae-9393265-1fa400-166f0b27b0da68; __tasessionId=oqgf18z8e1545731250994; CNZZDATA1259612802=986149189-1520427358-https%253A%252F%252Fwww.baidu.com%252F%7C1545731302'}
    param = {'max_behot_time': '0'}
    get_data(param, root_url, headers)


