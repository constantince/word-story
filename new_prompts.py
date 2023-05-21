#0. 定义格式
formater = """
Now, we will play a game. All your responese should follow the format that provided at the end
of each prompt.

"""

#1. 创建故事梗概
outline_of_the_story = """
Write an outline of a engaing story for me about {topic}. 
This story has {chapter_num} chapters, and then list all chapter titles for me.
Also need the heros of the story.

The format should be like this:
Outline: xxxxx;
Heros: xxxxx;
Chapter X: xxxxx;
"""

#2. 编写其他的章节
continue_the_story = """
Given the outline and the chapters of an story:

{outline}

And now we are in chapter{c1}
Pick up randomly words from below list to finish this chapter.
{key_words}

Do not tell the ending of the story or wrap up the story.

"""


#2.5 编写其他的章节如果没有单词了
continue_the_story_without_words = """
Given the outline and chapters of an story:

{outline}

And now we are in chapter{c1}

continue the story and finish this chapter.

Do not tell the ending of the story or wrap up the story.

"""

#3. 上个章节的End status
end_chapter_status = """
Given the ouline and chapters of a story:
{outline}
and given the previous chapter:
{chapter}
1. Summary what happended in previous chapter.
2. Give me the end stats where you list the details of where the characters are, all characters mentioned.
3. Give The progress of the entire story.
The format should be like this:
Summary: xxxxxxxx
End stats: xxxxxxxx
Progress: xxxxxxx
"""

#1. 第一章
first_chapter_the_story = """
Given the outline and the chapters of an story:

{outline}

And now we are in chapter1

Pick up randomly words from below list to finish this chapter.

{key_words}

Do not tell the ending of the story or wrap up the story.
"""

#2. 最后一章
last_chapter_the_story = """
Given the outline and the chapters of an story:

{outline}

Then give me the last chapter of the story. 

From the words below, using all words to finish entire story.

{key_words}

Do tell the ending of the story and wrap up the story.

"""

#2.5 最后一章如果没有其他单词了
last_chapter_the_story_without_words = """
Given the outline and the chapters of an story:

{outline}

Then give me the last chapter of the story. 

Do tell the ending of the story and wrap up the story.

"""

