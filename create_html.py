import re
from words import words2, words, words1

def create_bold_html(word_list, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    for word in word_list:
        bold_word = f"<b>{word}</b>"
        text = re.sub(rf"(\b{word}\b)", bold_word, text, flags=re.IGNORECASE)

     # 将连续的换行符替换为新的段落
    text = re.sub(r'\n+', '</p><p>', text)
    html_output = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>title</title>
</head>
<body>
    <p>{text}</p>
</body>
</html>
"""
    with open("output.html", "w", encoding='utf-8') as file:
        file.write(html_output)

    print("HTML 文件已生成：output.html")





if __name__ == "__main__":
   create_bold_html(words1, "story_of_gods_new.txt")