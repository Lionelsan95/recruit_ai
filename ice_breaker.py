from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":

    print("Hello Langchain")

    summary_templates = """
        given in a json format the linkedin profile {information} about a person from I want you to create : 
        1. a short summary
        2. two interesting facts about them
    """

    # summary_prompt_template = PromptTemplate.from_template(summary_templates)
    summary_prompt_template = PromptTemplate(
        input_variables={"information"}, template=summary_templates
    )
    summary_prompt_template.format(information="information")

    #llm = ChatOpenAI(temperature=0, model_name="davinci-002")
    llm = ChatOllama(model='llama3.2')

    chain = summary_prompt_template | llm | StrOutputParser()

    information = scrape_linkedin_profile(linkedin_profile_url='https://www.linkedin.com/in/skalskip92/', mock=True)
    res = chain.invoke(input={"information": information})

    print(res)
