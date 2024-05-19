
# prompt_templates.py

from langchain.prompts import PromptTemplate

# Template for system messages
system_message_template = PromptTemplate(
    input_variables=["behavior", "company", "persona"],
    template="{behavior}\n\n{company}\n\n{persona}"
)

# Template for human messages
human_message_template = PromptTemplate(
    input_variables=["content"],
    template="{content}"
)

# Template for AI messages
ai_message_template = PromptTemplate(
    input_variables=["response"],
    template="{response}"
)
