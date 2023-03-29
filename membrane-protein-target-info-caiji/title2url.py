import sys
import urllib.parse

# 获取要转换的文章标题文件名
title_filename = 'titles.txt'

# 读取文章标题列表
with open(title_filename, "r") as f:
    titles = [line.strip() for line in f]

# Open the output file for writing
with open("urlss.tsv", "w") as output_file:
    # 循环遍历标题列表，将每个标题转换为 Google Scholar 链接并打印
    for title in titles:
        # 将标题进行 URL 编码
        encoded_title = urllib.parse.quote(title)

        # 生成目标 URL
        url = f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={encoded_title}&btnG="

        # Write the generated URL to the output file
        output_file.write(url + "\n")
