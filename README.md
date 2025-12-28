1.https://lrc-maker.github.io/#/synchronizer/将歌曲文件和歌词文件放到该网站，生成lrc文件

2.将lrc文件和MP3，传到代码中

3.代码需要下载 pydub库和ffmpeg，
    pydub库：pip install
    ffmpeg:参照(https://blog.csdn.net/qq_43210277/article/details/156222085)
      在代码中强制指定路径:
       # 强制设置ffmpeg路径
        FFMPEG_BIN = r"D:/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"
        FFPROBE_BIN = r"D:/ffmpeg-7.1.1-essentials_build/bin/ffprobe.exe"
        # 强制设置 pydub 依赖路径
        AudioSegment.converter = FFMPEG_BIN
        AudioSegment.ffprobe = FFPROBE_BIN
        os.environ["PATH"] += os.pathsep + os.path.dirname(FFMPEG_BIN)
        
4.运行即可，需要剪断的语句音频全部存入代码文件位置下的output文件夹
<img width="799" height="202" alt="1" src="https://github.com/user-attachments/assets/e0edc310-102c-4894-a454-215929562d0e" />
<img width="844" height="508" alt="2" src="https://github.com/user-attachments/assets/713623a7-2dfe-4bf8-ab95-192a0c189e50" />

