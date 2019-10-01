import requests
import re
import os
import subprocess

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

root = 'D://bilibili视频//'
avid = 'av58300932'
sub_root = root + avid + '//'
merge_root = root + avid + '//视频音频合并目录//'

root_url = 'https://www.bilibili.com/video/' + avid
root_res = requests.get(root_url, headers=headers)

root_regex = re.compile(r'<span class="cur-page">(.*?)</span>')
page_num = int(re.findall(r'.*/(.*)', root_regex.findall(root_res.text)[0])[0])
print("page:", page_num)

if not os.path.exists(root):
    os.mkdir(root)
if not os.path.exists(sub_root):
    os.mkdir(sub_root)
if not os.path.exists(merge_root):
    os.mkdir(merge_root)
for i in range(page_num):
    video_file = sub_root + str(i + 1) + '.mp4'
    audio_file = sub_root + str(i + 1) + '.mp3'
    out_file = merge_root + str(i + 1) + '.mp4'
    subprocess.call('ffmpeg -i ' + video_file + ' -i ' + audio_file + ' -strict -2 -f mp4 ' + out_file, shell=True)
