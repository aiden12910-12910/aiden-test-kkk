import json
import yt_dlp

# 在这里输入你想追踪的 YouTube 创作者的 Shorts 页面
CHANNELS = [
    "https://youtube.com",
    "https://youtube.com"
]

def get_shorts_stream_url(channel_url):
    ydl_opts = {
        'playlistend': 5,      # 每个创作者获取最新的 5 个短视频
        'skip_download': True, # ⭐ 核心改变：全在云端运行，只拿视频流直链，不下载文件
        'extract_flat': False, 
        'format': 'mp4/best',  # 只要 mp4 格式，方便 Chromebook 播放
        'quiet': False,        # 开启日志，方便查看 Action 运行状态
        
        # ⭐ 顶级反爬伪装：强行伪装成智能电视和嵌入式网页客户端，绕过 GitHub 节点的 IP 限制
        'extractor_args': {
            'youtube': {
                'player_client': ['tv', 'web_embedded', 'ios']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
    }
    
    video_list = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"\n[Actions 抓取] 正在请求: {channel_url}")
            info = ydl.extract_info(channel_url, download=False)
            
            if info and 'entries' in info:
                for entry in info['entries']:
                    if not entry: continue
                    
                    # 过滤非短视频（长视频不适合滚动刷）
                    duration = entry.get('duration', 0)
                    if duration and duration > 60:
                        continue
                        
                    video_list.append({
                        "title": entry.get('title', '无标题'),
                        "video_url": entry.get('url'),  # 直链会由 Actions 定时刷新，保持可用
                        "thumbnail": entry.get('thumbnail'), 
                        "author": info.get('uploader', '未知创作者')
                    })
        except Exception as e:
            print(f"[错误] 抓取 {channel_url} 失败: {e}")
    return video_list

if __name__ == "__main__":
    all_shorts = []
    for channel in CHANNELS:
        all_shorts.extend(get_shorts_stream_url(channel))
    
    # 写入 data.json 供前端 index.html 读取
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_shorts, f, ensure_ascii=False, indent=4)
        
    print(f"\n[云端生成完毕] 成功抓取到 {len(all_shorts)} 个视频链接。")
