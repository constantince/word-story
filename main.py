from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from prompts import outline_of_the_story, conflict_of_the_story, heros_of_the_story, first_parts_of_the_story, previous_story_summary,continue_the_story
from langchain.memory import SimpleMemory
from words import words2, words
from langchain.chains import ConversationChain
from langchain.memory import ChatMessageHistory
from langchain.chains import SimpleSequentialChain, SequentialChain
from langchain.schema import messages_from_dict, messages_to_dict
import time
import os

def remove_words_in_text(text, word_list):
    words = text.lower().split()
    remaining_words = [word for word in word_list if word.lower() not in words]
    
    return remaining_words


os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

allwords = words

timestamp = int(time.time())
filename = "story_of_gods.txt"



llm = OpenAI(temperature=0.7, max_tokens=1000, verbose=True)


prompt_template = PromptTemplate(input_variables=["topic"], template=outline_of_the_story)
outline_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="outline")

prompt_template2 = PromptTemplate(input_variables=["outline"], template=conflict_of_the_story)
conflict_chain = LLMChain(llm=llm, prompt=prompt_template2, output_key="conflict")

prompt_template3 = PromptTemplate(input_variables=["outline", "conflict"], template=heros_of_the_story)
hero_chain = LLMChain(llm=llm, prompt=prompt_template3, output_key="heros")


outline_chain = SequentialChain(
    chains=[outline_chain, conflict_chain, hero_chain],
    verbose=True,
    input_variables=["topic"],
    output_variables=["outline", "conflict", "heros"]
    )

# 写章节的记忆，前情提要，主角，冲突等
memory = outline_chain({"topic": "Ancient Greece God"});
print(memory)
#---------------------------------------------------------------------------
# 开始编写首个章节

llm2 = OpenAI(temperature=0.7, max_tokens=3000, verbose=True)

prompt_template4 = PromptTemplate(input_variables=["outline", "conflict", "heros", "key_words"], template=first_parts_of_the_story)
part_chain = LLMChain(llm=llm2, prompt=prompt_template4, output_key="part")

prompt_template5 = PromptTemplate(input_variables=["part"], template=previous_story_summary)
summary_chain = LLMChain(llm=llm2, prompt=prompt_template5, output_key="privous")


chapter_chain = SequentialChain(
    memory=SimpleMemory(memories=memory),
    chains=[part_chain, summary_chain],
    input_variables=["key_words"],
    # Here we return multiple variables
    output_variables=["part","privous"],
    verbose=True
    )

first_chapter = chapter_chain({"key_words": ', '.join(allwords)})


allwords = remove_words_in_text(first_chapter["part"], allwords)

print("first part###########################################", first_chapter["part"])
with open(filename, "a") as file:
    file.write(first_chapter["part"])
    file.write("\n")  # This line adds a newline character at the end, so the next appended text starts on a new line
#------------------------------------------------------------------------------------
# 开始编写剩余的章节

llm3 = OpenAI(temperature=1.3, max_tokens=3000, verbose=True)

prevous = first_chapter["privous"]

while True:
    prompt_template6 = PromptTemplate(input_variables=["outline", "conflict", "heros", "key_words", "privous"], template=continue_the_story)
    continue_chain = LLMChain(llm=llm3, prompt=prompt_template6, output_key="part")
    
    prompt_template7 = PromptTemplate(input_variables=["part"], template=previous_story_summary)
    continue_summary_chain = LLMChain(llm=llm3, prompt=prompt_template7, output_key="fornext")
    
    
    continue_overall_chain = SequentialChain(
        memory=SimpleMemory(memories=memory),
        chains=[continue_chain, continue_summary_chain],
        input_variables=["privous", "key_words"],
        # Here we return multiple variables
        output_variables=["part", "fornext"],
        verbose=True
        )
    
    
    continues = continue_overall_chain({"key_words": ', '.join(allwords), "privous": prevous})
    
    print("########################################", continues["part"])
    
    with open(filename, "a") as file:
        file.write(continues["part"])
        file.write("\n")  # This line adds a newline character at the end, so the next appended text starts on a new line
    
    prevous = continues["fornext"]
    allwords = remove_words_in_text(continues["part"], allwords)
    print("remained words", allwords)
    if len(allwords) < 1:
        break;



print("done........")






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