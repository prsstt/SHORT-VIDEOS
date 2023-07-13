import openai
import csv

# Set up your OpenAI API key
openai.api_key_path = "secret.txt"
#Prompts
prompt2 = ""
prompt1_path = "prompts/prompt1.txt"
prompt2_path = "Okay, I want the quotes to be about" + prompt2
prompt3_path = "prompts/prompt3.txt"
prompt4_path = "Perfect, now i want you to write 30 different quotes about" + prompt2 + "in the same style."
# Define the prompts
messages = [{"role": "user", "content": prompt1_path}]

prompt2 = input("Topics/themes:")