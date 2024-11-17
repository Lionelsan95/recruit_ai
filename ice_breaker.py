from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup


def fetch_linkedin_profile_data(name: str) -> str:
    linkedin_query = f"{name} LinkedIn"
    linkedin_profile_url = lookup(name=linkedin_query)

    print(f"The profile url of {name} is : {linkedin_profile_url}")

    information = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_profile_url, mock=True
    )

    return information


def generate_ice_break(information: str) -> str:

    summary_templates = """
        You are an experienced HR in tech industry
        given in a json format the linkedin profile {information} about a person from I want you to firstly analyze the whole json file to clearly understand the structure and all links about. After all that create : 
        1. a short summary
        2. two interesting facts about them
        3. what can be the next position for him in the futur
        4. which countres could the best option for work with his profile
    """

    # summary_prompt_template = PromptTemplate.from_template(summary_templates)
    summary_prompt_template = PromptTemplate(
        input_variables={"information"}, template=summary_templates
    )
    summary_prompt_template.format(information="information")

    llm = ChatOllama(model="llama3.2")

    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={"information": information})

    return res


if __name__ == "__main__":

    print("==> Ice Breaker with Langchain <==")

    name = input("Please enter your name: ")

    information = fetch_linkedin_profile_data(name)

    res = generate_ice_break(information)

    print(res)
