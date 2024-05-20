import requests
import streamlit as st

API_ENDPOINT = "https://devapi.beyondchats.com/api/get_message_with_sources"

def fetch_data_from_api():
    data = []
    page = 1
    while True:
        params = {'page': page}
        response = requests.get(API_ENDPOINT, params=params)
        if response.status_code == 200:
            response_json = response.json()
            if 'data' in response_json and 'data' in response_json['data']:
                page_data = response_json['data']['data']
                if not page_data:
                    break
                data.extend(page_data)
                page += 1
            else:
                st.error(f"API response is not in the expected format. Response: {response_json}")
                break
        elif response.status_code == 429:
            st.warning("API rate limit exceeded. Please wait and try again later.")
            break
        else:
            st.error(f"Failed to fetch data from API. Status code: {response.status_code}")
            break
    return data

def identify_citations(response_text, sources):
    citations = []
    for source in sources:
        if isinstance(source, dict) and 'context' in source and 'id' in source:
            if source['context'] in response_text:
                citations.append({
                    'id': source['id'],
                    'link': source.get('link', '')
                })
    return citations

def main():
    st.title("Response Citations Checker")

    # Fetch data from API
    st.write("Fetching data from API...")
    data = fetch_data_from_api()

    st.write(f"Fetched {len(data)} items from the API.")

    # Displaying results
    st.subheader("Results:")

    for item in data:
        if isinstance(item, dict) and 'response' in item and 'source' in item:
            response_text = item['response']
            sources = item['source']

            citations = identify_citations(response_text, sources)

            st.write("Response Text:")
            st.write(response_text)
            st.write("Citations (Sources):")
            if citations:
                for citation in citations:
                    st.write(f"- ID: {citation['id']}, Link: {citation['link']}")
            else:
                st.write("No citations found.")

            st.write("---")
        else:
            st.warning(f"Unexpected format for item: {item}")

if __name__ == "__main__":
    main()
