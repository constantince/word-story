from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from new_prompts import outline_of_the_story, first_chapter_the_story, end_chapter_status, continue_the_story,continue_the_story_without_words, last_chapter_the_story, last_chapter_the_story_without_words
from langchain.memory import SimpleMemory
from words import words2, words, words1
from langchain.chains import ConversationChain
from langchain.memory import ChatMessageHistory
from langchain.chains import SimpleSequentialChain, SequentialChain
from langchain.schema import messages_from_dict, messages_to_dict
import query
import time
import math
import os
import re

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")


def remove_words_in_text(text, word_list):
    words = text.lower().split()
    remaining_words = [word for word in word_list if word.lower() not in words]
    
    return remaining_words
    
def create_bold_html(word_list, text):
    for word in word_list:
        bold_word = f"<b>{word}</b>"
        text = re.sub(rf"(\b{word}\b)", bold_word, text, flags=re.IGNORECASE)

     # 将连续的换行符替换为新的段落
    text = re.sub(r'\n+', '</p><p>', text)
    html_output = f"""
        <body>
            <p>{text}</p>
        </body>

    """
    return html_output

def llm_core_tell_story(word_list, topic, filename):
    
    story_text = ""
    
    allwords = word_list

    llm = OpenAI(temperature=1.1, max_tokens=3000, verbose=True)
    
    
    prompt_outline_chapters = PromptTemplate(input_variables=["topic", "chapter_num"], template=outline_of_the_story)
    chain_outline_chapters = LLMChain(llm=llm, prompt=prompt_outline_chapters, output_key="outline")
    
    outline_chain = SequentialChain(
        chains=[chain_outline_chapters],
        verbose=True,
        input_variables=["topic", "chapter_num"],
        output_variables=["outline"]
        )
    
    # 写章节的章节数：
    array_length = len(word_list)
    result = math.ceil(array_length / 10) + 3
    
    memory = outline_chain({"topic": topic, "chapter_num": result});
    
    
    print(memory)
    #---------------------------------------------------------------------------
    # 开始编写首个章节
    
    llm2 = OpenAI(temperature=0.7, max_tokens=2000, frequency_penalty=1, verbose=True)
    
    prompt_first_chapter = PromptTemplate(input_variables=["outline", "key_words"], template=first_chapter_the_story)
    chain_first_chapter = LLMChain(llm=llm2, prompt=prompt_first_chapter, output_key="chapter")
    
    prompt_end_stats = PromptTemplate(input_variables=["outline", "chapter"], template=end_chapter_status)
    chain_end_stats = LLMChain(llm=llm2, prompt=prompt_end_stats, output_key="stats")
    
    # prompt_template5 = PromptTemplate(input_variables=["part"], template=previous_story_summary)
    # summary_chain = LLMChain(llm=llm2, prompt=prompt_template5, output_key="privous")
    
    
    chapter_chain = SequentialChain(
        memory=SimpleMemory(memories=memory),
        chains=[chain_first_chapter, chain_end_stats],
        input_variables=["key_words"],
        # Here we return multiple variables
        output_variables=["chapter", "stats"],
        verbose=True
        )
    
    first_chapter = chapter_chain({"key_words": ', '.join(allwords)})
    
    
    allwords = remove_words_in_text(first_chapter["chapter"], allwords)
    
    print("first part###########################################", first_chapter["chapter"])
    story_text +=  first_chapter["chapter"] + '\n'
    # with open(filename, "a") as file:
    #     file.write(first_chapter["chapter"])
    #     file.write("\n")  # This line adds a newline character at the end, so the next appended text starts on a new line
    # #------------------------------------------------------------------------------------
    # 开始编写剩余的章节
    
    llm3 = OpenAI(temperature=0.8, max_tokens=2000, frequency_penalty=1.2, verbose=True)
    
    previous = first_chapter["stats"]
    
    for i in range(result - 2):
        
        print("chapter", i+2, " started")
        
        if len(allwords) > 0:
            prompt_continue = PromptTemplate(input_variables=["outline", "key_words", "c1"], template=continue_the_story)
            continue_chain = LLMChain(llm=llm3, prompt=prompt_continue, output_key="chapter")
        else:
            prompt_continue = PromptTemplate(input_variables=["outline", "c1"], template=continue_the_story_without_words)
            continue_chain = LLMChain(llm=llm3, prompt=prompt_continue, output_key="chapter")
            
            
        chain_end_stats = PromptTemplate(input_variables=["outline", "chapter"], template=end_chapter_status)
        continue_summary_chain = LLMChain(llm=llm3, prompt=chain_end_stats, output_key="stats")
        
        
        continue_overall_chain = SequentialChain(
            memory=SimpleMemory(memories=memory),
            chains=[continue_chain, continue_summary_chain],
            input_variables=["key_words", "c1"],
            # Here we return multiple variables
            output_variables=["chapter", "stats"],
            verbose=True
            )
        
        
        continues = continue_overall_chain({"key_words": ', '.join(allwords), "before": previous, "c1": i+2, "c2": i+3})
        
        print("########################################", continues["chapter"])
        
        story_text +=  continues["chapter"] + '\n'
        
        # with open(filename, "a") as file:
        #     file.write(continues["chapter"])
        #     file.write("\n")  # This line adds a newline character at the end, so the next appended text starts on a new line
        
        previous = continues["stats"]
        allwords = remove_words_in_text(continues["chapter"], allwords)
        
        print("\n remained words:", allwords)
        
        
        
    # 最后一章
    
    if len(allwords) > 0:
        prompt_last = PromptTemplate(input_variables=["outline", "key_words"], template=last_chapter_the_story)
        last_chain = LLMChain(llm=llm3, prompt=prompt_last, output_key="chapter")
    else:
        prompt_last = PromptTemplate(input_variables=["outline"], template=last_chapter_the_story_without_words)
        last_chain = LLMChain(llm=llm3, prompt=prompt_last, output_key="chapter")
        
        
        
    last_overall_chain = SequentialChain(
        memory=SimpleMemory(memories=memory),
        chains=[last_chain],
        input_variables=["key_words"],
        # Here we return multiple variables
        output_variables=["chapter"],
        verbose=True
        )
    
    
    last = last_overall_chain({"key_words": ', '.join(allwords), "before": previous})
    
    print("last chapter ########################", last["chapter"])
    
    # with open(filename, "a") as file:
    #     file.write(last["chapter"])
    #     file.write("\n")  # This line adds a newline character at the end, so the next appended text starts on a new line
        
    story_text +=  last["chapter"] + '\n'
    
    allwords = remove_words_in_text(last["chapter"], allwords)
    
    print("\n remained words:", allwords)
    
    return story_text
    
def outputHtml(allwords, topic, uid):
    # 生成故事内容
    text = llm_core_tell_story(allwords, topic)
    # 生产html片段
    html = create_bold_html(allwords, text)
    # 更新数据库
    query.updateStory(uid=uid, content=html, status=1)
    
# while True:
#     prompt_template6 = PromptTemplate(input_variables=["outline", "conflict", "heros", "key_words", "privous"], template=continue_the_story)
#     continue_chain = LLMChain(llm=llm3, prompt=prompt_template6, output_key="part")
    
#     prompt_template7 = PromptTemplate(input_variables=["part"], template=previous_story_summary)
#     continue_summary_chain = LLMChain(llm=llm3, prompt=prompt_template7, output_key="fornext")
    
    
#     continue_overall_chain = SequentialChain(
#         memory=SimpleMemory(memories=memory),
#         chains=[continue_chain, continue_summary_chain],
#         input_variables=["privous", "key_words"],
#         # Here we return multiple variables
#         output_variables=["part", "fornext"],
#         verbose=True
#         )
    
    
#     continues = continue_overall_chain({"key_words": ', '.join(allwords), "privous": prevous})
    
#     print("########################################", continues["part"])
    
#     with open(filename, "a") as file:
#         file.write(continues["part"])
#         file.write("\n")  # This line adds a newline character at the end, so the next appended text starts on a new line
    
#     prevous = continues["fornext"]
#     allwords = remove_words_in_text(continues["part"], allwords)
#     print("remained words", allwords)
#     if len(allwords) < 1:
#         break;



# print("done........")






# history = ChatMessageHistory()


# # 1. 开始设定故事的梗概和背景
# prompt = PromptTemplate(
#     input_variables=["topic"],
#     template=outline_of_the_story
# )

# history.add_user_message(prompt.format(topic="universe"))

# chain = LLMChain(llm=llm, prompt=prompt)

# result = chain.run("universe")

# history.add_ai_message(result)

# dicts = messages_to_dict(history.messages)

# print(dicts)