import requests
import re
import json
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Referer': 'https://www.bilibili.com/video/av58300932/'
}
avid = 'av58300932'
root_url = 'https://www.bilibili.com/video/' + avid
root_res = requests.get(root_url, headers=headers)

root_regex = re.compile(r'<span class="cur-page">(.*?)</span>')
#print(root_regex.findall(root_res.text))
#print(re.findall(r'.*/(.*)', root_regex.findall(root_res.text)[0]))
page_num = int(re.findall(r'.*/(.*)', root_regex.findall(root_res.text)[0])[0])
print("page:", page_num)

root = 'D://bilibili视频//'
if not os.path.exists(root):
    os.mkdir(root)

sub_root = root + avid + '//'
if not os.path.exists(sub_root):
    os.mkdir(sub_root)

for i in range(page_num):
    sub_url = root_url + '/?p=' + str(i + 1)
    sub_res = requests.get(sub_url, headers=headers)
    print("sub_url:", sub_url)
    print("sub_res.status_code:", sub_res.status_code)

    regex = re.compile(r'<script>window.__playinfo__=(.*?)</script>')
    json_str = regex.findall(sub_res.text)[0]
    #print(regex.findall(sub_res.text)[0], i)
    url_json = json.loads(json_str)

    video_url = url_json['data']['dash']['video'][0]['baseUrl']
    video_res = requests.get(video_url, headers=headers, stream=True)
    print("video_url:", video_url)
    print("video_res.status_code:", video_res.status_code)

    video_file = str(i + 1) + '.mp4'
    with open(sub_root + video_file, 'wb') as f:
        f.write(video_res.content)

    audio_url = url_json['data']['dash']['audio'][0]['baseUrl']
    audio_res = requests.get(audio_url, headers=headers, stream=True)
    print("audio_url:", audio_url)
    print("audio_res.status_code:", audio_res.status_code)

    audio_file = str(i + 1) + '.mp3'
    with open(sub_root + audio_file, 'wb') as f:
        f.write(audio_res.content)

