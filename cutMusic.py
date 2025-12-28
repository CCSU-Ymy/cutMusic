import os
import re
from pydub import AudioSegment

FFMPEG_BIN = r"D:/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"
FFPROBE_BIN = r"D:/ffmpeg-7.1.1-essentials_build/bin/ffprobe.exe"

# 强制设置 pydub 依赖路径
AudioSegment.converter = FFMPEG_BIN
AudioSegment.ffprobe = FFPROBE_BIN
os.environ["PATH"] += os.pathsep + os.path.dirname(FFMPEG_BIN)


def parse_lrc(lrc_file_path):
    """解析LRC文件，返回 (时间ms, 歌词) 的列表"""
    with open(lrc_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    lyrics = []
    # 正则匹配 [mm:ss.xx] 格式
    pattern = re.compile(r'\[(\d{2}):(\d{2})\.(\d{2,3})\](.*)')
    
    for line in lines:
        match = pattern.match(line)
        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            # 处理2位或3位毫秒
            milliseconds = int(match.group(3)) if len(match.group(3)) == 3 else int(match.group(3)) * 10
            
            total_ms = (minutes * 60 * 1000) + (seconds * 1000) + milliseconds
            text = match.group(4).strip()
            # 过滤掉空的歌词行，或者元数据（如 作词：xxx）
            if text and "作词" not in text and "作曲" not in text: 
                lyrics.append((total_ms, text))
    return lyrics

def split_audio_by_lrc(mp3_path, lrc_path, output_folder="output"):
    # 1. 加载音频
    print(f"正在加载音频: {mp3_path} ...")
    audio = AudioSegment.from_mp3(mp3_path)
    
    # 2. 解析歌词
    lyrics = parse_lrc(lrc_path)
    if not lyrics:
        print("未找到有效的LRC歌词行")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print(f"共找到 {len(lyrics)} 句歌词，开始剪切...")

    for i in range(len(lyrics)):
        start_ms, text = lyrics[i]
        
        # 确定结束时间：
        # 如果不是最后一句，结束时间就是下一句的开始时间
        # 如果是最后一句，结束时间就是音频总长度
        if i < len(lyrics) - 1:
            end_ms = lyrics[i+1][0]
        else:
            end_ms = len(audio)
            
        # 剪切片段
        chunk = audio[start_ms:end_ms]
        
        # 处理文件名（去除非法字符）
        safe_text = re.sub(r'[\\/*?:"<>|]', "", text)
        filename = f"{i+1:03d}_{safe_text}.mp3"
        output_path = os.path.join(output_folder, filename)
        
        chunk.export(output_path, format="mp3")
        print(f"导出: {filename}")

    print("全部完成！")

# --- 使用配置 ---
# 修改这里的文件名为你的文件路径
mp3_file = "LaoJieXianQing.mp3"
lrc_file = "LaoJieXianQing.lrc" 

# 运行函数
if __name__ == '__main__':
    # 确保文件存在再运行
    if os.path.exists(mp3_file) and os.path.exists(lrc_file):
        split_audio_by_lrc(mp3_file, lrc_file)
    else:
        print("请检查文件夹下是否有对应的mp3和lrc文件，并修改脚本中的文件名。")