import json

from tools.get_html import GetHtml


class GetAppointSina:
    def __init__(self):
        self.since_id = ''
        self.comment_id = 0
        self.get_json = GetHtml()

    def get_blog(self, url, content_outfile_path,comment_outfile_path):
        while 1:
            try:
                url = url + '&since_id=' + self.since_id
                data = self.get_json.get_html(url)
                data_dict = json.loads(data)
                self.since_id = str(data_dict['data']['cardlistInfo']['since_id'])
                data_list = data_dict['data']['cards']
            except:
                break
            cont = open(content_outfile_path, 'a+', encoding='utf-8')
            for data0 in data_list:
                data1 = data0['mblog']
                if data1:
                    content_text = data1['text']
                    cont.write(content_text)
                    content_id = str(data1['id'])
                    self.get_comment(content_id,comment_outfile_path)

    def get_comment(self, content_id, comment_outfile_path):
        while 1:
            try:
                url = f'https://m.weibo.cn/comments/hotflow?id={content_id}&mid={content_id}&max={self.comment_id}&max_id_type=0'
                data2 = self.get_json.get_html(url)
                data2_dict = json.loads(data2)
                get_status = data2_dict['ok']
            except:
                break
            if not get_status:
                with open(comment_outfile_path + '\\..\\wrong.log', 'a+', encoding='utf-8') as f:
                    f.write(url)
                break
            data2_list = data2_dict['data']['data']
            for data2 in data2_list:
                self.comment_id = data2['id']
                comment_text = data2['text']
                f = open(comment_outfile_path, 'a+', encoding='utf-8')
                f.write(comment_text + '\n')
                comment_list = data2['comments']
                if not comment_list:
                    continue
                for comment in comment_list:
                    comment_text_text = comment['text']
                    f.write(comment_text_text + '\n')


if __name__ == '__main__':
    get_appoint_sina = GetAppointSina()
    url = 'https://m.weibo.cn/api/container/getIndex?uid=1703612533&luicode=10000011&lfid=100103type%3D1%26q%3DEskey%E7%9F%A5%E6%98%9F%E5%A4%A7%E9%94%85%E9%94%85&type=uid&value=1703612533&containerid=1076031703612533'
    content_outfile_path = 'C:\\Users\\v-seyan\\data\\content.txt'
    comment_outfile_path = 'C:\\Users\\v-seyan\\data\\comment.txt'
    get_appoint_sina.get_blog(url,content_outfile_path,comment_outfile_path)
