import os
import requests
from dotenv import load_dotenv


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    Scrape informations from linkedIn profile, Manually scrape the information from the linkedIn profile.
    """

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/Lionelsan95/ff57545813ff2fdc8e2315158fbc9369/raw/56654493a3995cd778d7cda7aeda3d57479c2e17/lionel_owono.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            os.environ.get("PROXYCURL_LINKEDIN_API_URL"),
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )

    data = clean_linkedin_json_data(response.json())

    return data


def clean_linkedin_json_data(data):

    # Clés et valeurs à exclure
    exclude_keys = {"people_also_viewed", "certifications"}
    empty_values = ([], "", None)

    # Filtrage des données
    cleaned_data = {
        k: v for k, v in data.items() if v not in empty_values and k not in exclude_keys
    }

    # Retirer 'profile_pic_url' de chaque groupe si "groups" est présent
    for group in cleaned_data.get("groups", []):
        group.pop("profile_pic_url", None)

    return cleaned_data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/skalskip92/", mock=True
        ),
    )
