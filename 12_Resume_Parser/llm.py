from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_ollama import ChatOllama


system_prompt = system_message = """
      You are an expert information extraction system specialized in parsing resumes into structured data.

      Your task is to extract relevant information from unstructured resume text and return it in strictly valid JSON format.

      ### Rules:
      - Output ONLY valid JSON. No explanations, no markdown, no extra text.
      - Ensure the JSON is syntactically correct and parsable.
      - If a field is missing, return null or an empty array [] (do not hallucinate).
      - Preserve original meaning but normalize formatting where appropriate.
      - Dates should be in a consistent readable format (e.g., "MMM YYYY" or "YYYY-MM").
      - Extract multiple entries as arrays (e.g., multiple experiences, projects, education entries).
      - Do NOT infer information that is not explicitly present.
      - Avoid duplication of entries.

      ### Output Schema:
      {{
        "contact_information": {{
          "name": string | null,
          "email": string | null,
          "phone_number": string | null,
          "website": string | null
        }},
        "education": [
          {{
            "institution_name": string | null,
            "degree": string | null,
            "field_of_study": string | null,
            "graduation_dates": string | null
          }}
        ],
        "experience": [
          {{
            "job_title": string | null,
            "company_name": string | null,
            "location": string | null,
            "dates_of_employment": string | null,
            "responsibilities": [string]
          }}
        ],
        "projects": [
          {{
            "project_title": string | null,
            "description": string | null,
            "technologies_used": [string],
            "outcomes": string | null
          }}
        ],
        "skills": {{
          "programming_languages": [string],
          "technologies_tools": [string]
        }},
        "additional_information": {{
          "certifications": [string],
          "awards": [string],
          "affiliations": [string],
          "languages": [string]
        }}
      }}

      Return only the JSON object.
"""
human_prompt = """
  Extract structured resume data from the following text.

  Resume Text:
  {context}
"""
json_prompt = """
      Please validate and correct the following JSON data:
      **Extracted Information:**

      {data}

      Provide only the corrected JSON, with no preamble or explanation.
      **Corrected JSON:**
"""


OLLAMA_BASE_URL="http://localhost:11434/"
GEMMA_MODEL = "gemma3:4b"

ollama_llm = ChatOllama(
  model=GEMMA_MODEL,
  base_url=OLLAMA_BASE_URL,
  validate_model_on_init=True
)

system_message = SystemMessagePromptTemplate.from_template(system_prompt)
human_message = HumanMessagePromptTemplate.from_template(human_prompt)

def ask_llm(context):
  messages = [system_message, human_message]
  final_message = ChatPromptTemplate(messages)
  chain = final_message | ollama_llm | StrOutputParser()

  return chain.invoke({'context': context})


def validate_json(data):
  human_message = HumanMessagePromptTemplate.from_template(json_prompt)
  messages = [human_message]
  final_message = ChatPromptTemplate(messages)

  chain = final_message | ollama_llm | JsonOutputParser()
  return chain.invoke({"data": data})
