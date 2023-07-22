import ffmpeg
import os
import pandas as pd
from natsort import natsorted

durations_sum = 0

def is_video_file(file_path):
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov']  # 读取的文件扩展名
    ext = os.path.splitext(file_path)[1]
    return ext.lower() in video_extensions
    
def get_video_duration(file_path):
    # 在函数内部读取视频时长并累加到全局变量 durations_sum
    global durations_sum
    probe = ffmpeg.probe(file_path)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
    duration = float(video_info['duration'])
    durations_sum += duration
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    return hours, minutes, seconds


folder_path = '/Users/leeda/Desktop/考研/数学/周洋鑫/'  # 替换为你要遍历的文件夹路径
replace_str = "【后续完整更新+VX：yxmm2024，公众号：研学木木】" # 重命名文件 不必要的内容
file_names = []
video_durations = []

for root, dirs, files in sorted(os.walk(folder_path)):
        dirs = natsorted(dirs, key=lambda x: x.replace('.', '~')+'z')
        files = natsorted(files, key=lambda x: x.replace('.', '~')+'z')
        for file in files:
            if file == ".DS_Store" or "数一" in file:
                continue  # 跳过 .DS_Store 文件
            file_path = os.path.join(root, file)
            os.rename(file_path, file_path.replace(replace_str,""))

            # file_names.append(file_path.replace(folder_path,"").replace(replace_str,""))
            print(file_path)
            # print(root,dirs)
            if is_video_file(file_path):
                hours, minutes, seconds = get_video_duration(file_path)
                video_durations.append(f"{hours}时{minutes}分{seconds}秒")
                file_names.append(file_path.replace(folder_path,"").replace(replace_str,""))
            else:
                 print(file_path)
                #  video_durations.append(" ")

# 创建数据框
data = pd.DataFrame({'文件名': file_names,'视频时长': video_durations })

hours_sum = int(durations_sum // 3600)
minutes_sum = int((durations_sum % 3600) // 60)
seconds_sum = int(durations_sum % 60)
print(f"共计{hours_sum}时 {minutes_sum}分{seconds_sum}秒")

# 保存为 Excel 文件
output_path = 'video_files.xlsx'
data.to_excel(output_path, index=False)

print(f"文件已导出为 {output_path}")
