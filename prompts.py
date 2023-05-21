#0. 定义格式
formater = """
Now, we will play a game. All your responese should follow the format that provided at the end
of each prompt.

"""

#1. 创建故事梗概
outline_of_the_story = """
Write an outline of a engaing story for me about {topic}.
"""

#2. 背景创作
conflict_of_the_story = """
Given the outline and chapters of a story:
{outline}
write the The main conflict of the story.
"""

#3. 主角的姓名和特点
heros_of_the_story = """
Here is a outline of a story:
{outline}
Given the conflict of the story:
{conflict}
write down the expected all the name of heros and their characteristics.
"""



#4 首个章节和部分
first_parts_of_the_story ="""
Given a story outline:
{outline}
and the conflict:
{conflict}
and the heros intro:
{heros}
From the words below, choose the ones you think are suitable and strongly related to write first part of the story.
{key_words}
"""

#5. 前情提要
previous_story_summary = """
summary this text:
{part}
"""


#6. 编写其他的章节
continue_the_story = """
Given a story outline:
{outline}
and the conflict:
{conflict}
and the heros intro:
{heros}
and privous summary:
{privous}
From the words below, choose the ones you think are suitable and strongly related to continue the story.
{key_words}
"""

