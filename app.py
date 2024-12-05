from flask import Flask, render_template, request
import requests
import ssl
import socket
from urllib.parse import urlparse
import openai

app = Flask(__name__)

# 1. HTTPS Check
def check_https(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme == "https"

# 2. SSL/TLS Certificate Validation
def check_ssl_certificate(url):
    hostname = urlparse(url).hostname
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            return cert  
        
# 3. IP Address and Geolocation
def get_ip_geolocation(api_key, url):
    # Extract the hostname from the URL
    hostname = url.split("//")[-1].split("/")[0]

    try:
        # Get the IP address of the hostname
        ip_address = socket.gethostbyname(hostname)
    except Exception as e:
        return {"error": f"Error resolving IP address: {e}"}

    # IPStack API endpoint
    api_url = f"http://api.ipstack.com/{ip_address}?access_key={api_key}"

    try:
        # API request
        response = requests.get(api_url)
        if response.status_code == 200:
            geo_data = response.json()
            return {
                "ip_address": ip_address,
                "country": geo_data.get("country_name"),
                "region": geo_data.get("region_name"),
                "city": geo_data.get("city"),
                "latitude": geo_data.get("latitude"),
                "longitude": geo_data.get("longitude")
            }
        else:
            return {"error": f"Error: {response.status_code}, {response.text}"}
    except Exception as e:
        return {"error": f"Error connecting to IPStack API: {e}"}

# 4. URL Reputation and Phishing Detection
def check_url_reputation(key, url_to_check):
    # Endpoint URL
    url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

    # API key
    api_key = key

    # Headers
    headers = {
        "Content-Type": "application/json"
    }

    # Payload
    payload = {
        "client": {
            "clientId": "URL Safety Checker",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],       
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url_to_check}
            ]
        }
    }

    params = {"key": api_key}

    response = requests.post(url, headers=headers, json=payload, params=params)

    # return"Status Code:", response.status_code)
    if response.status_code == 200:
        return "Response JSON:", response.json()
    else:
        return "Error:", response.text





def analyze_single_website(results):
    """
    Generates an analysis of a single website using OpenAI's ChatGPT API.

    :param results: A dictionary containing all the collected safety data for a URL.
    :return: Generated analysis from ChatGPT.
    """

    #OpenAI API Key
    openai.api_key = "OPENAI_API_KEY"
    prompt = f"""
    Analyze the safety and security of the following website based on the provided details:

    HTTPS Check: {results['https_check']}
    SSL Certificate Validation: {results['ssl_certificate']}
    Geolocation: {results['geolocation']}
    Google Safe Browsing Result: {results['url_reputation']}
    Based on this data, provide a detailed, firm analysis of whether the website is safe or unsafe. Your response must start with either "Safe" or "Unsafe", followed by a detailed explanation in paragraph form. If the Google Safe Browsing result is empty, assume it is not flagged in the database, but base your determination of safety on the other aspects provided (HTTPS check, SSL certificate, and geolocation).

    Do not use phrases like "further analysis is required" or "maybe." If any aspect of the data suggests the website is unsafe, state "Unsafe" and provide a clear explanation. If all aspects indicate the website is safe, state "Safe" and explain why. Avoid hallucinating data or providing assumptions not explicitly based on the provided input.

    Your analysis must be clear, professional, and concise but elaborate enough to provide a 250-word assessment.
    """


    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a security expert providing detailed analysis of website safety."},
                {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response['choices'][0]['message']['content']

def get_domain_age(api_key, url):
    """
    Get the registration age of a domain using Whois API.
    """
    domain = url.split("//")[-1].split("/")[0]
    api_url = f"https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={api_key}&domainName={domain}&outputFormat=JSON"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            creation_date = data.get("WhoisRecord", {}).get("createdDate", "Unknown")
            return f"Domain Creation Date: {creation_date}"
        else:
            return f"Error fetching domain info: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
    
def analysis(url):
        results = {}
     #HTTPS Check
        results["https_check"] = check_https(url)

        #SSL Certificate Validation
        try:
            results["ssl_certificate"] = check_ssl_certificate(url)
        except Exception as e:
            results["ssl_certificate"] = {"error": str(e)}

        #Geolocation Check
        try:
            api_key = "IPSTACK_API_KEY"
            results["geolocation"] = get_ip_geolocation(api_key, url)
        except Exception as e:
            results["geolocation"] = {"error": str(e)}

        #URL Reputation Check
        try:
            key = "GOOGLE_SAFE_BROWSING_URL_API"
            results["url_reputation"] = check_url_reputation(key, url)
        except Exception as e:
            results["url_reputation"] = {"error": str(e)}

        #ChatGPT Analysis
        chatgpt_analysis = analyze_single_website(results)

        return chatgpt_analysis, results

def comparitive_analysis(chatgpt_analysis1, chatgpt_analysis2, results1, results2):
    """
    Generate a comparative analysis of two URLs using ChatGPT.

    :param chatgpt_analysis1: ChatGPT analysis for URL 1
    :param chatgpt_analysis2: ChatGPT analysis for URL 2
    :param results1: Results dictionary for URL 1
    :param results2: Results dictionary for URL 2
    :return: Comparative analysis as a string
    """
    openai.api_key = "OPENAI_API_KEY"
    prompt = f"""
    Compare the safety and security of the following two websites based on their analyses and results:

    Website 1:
    ChatGPT Analysis: {chatgpt_analysis1}
    HTTPS Check: {results1.get('https_check', 'Unknown')}
    SSL Certificate Validation: {results1.get('ssl_certificate', 'Unknown')}
    Geolocation: {results1.get('geolocation', 'Unknown')}
    Google Safe Browsing Result: {results1.get('url_reputation', 'No data')}

    Website 2:
    ChatGPT Analysis: {chatgpt_analysis2}
    HTTPS Check: {results2.get('https_check', 'Unknown')}
    SSL Certificate Validation: {results2.get('ssl_certificate', 'Unknown')}
    Geolocation: {results2.get('geolocation', 'Unknown')}
    Google Safe Browsing Result: {results2.get('url_reputation', 'No data')}

    Highlight patterns, similarities, and differences in their safety features. Conclude with a clear statement on which website is safer and why, or if they are equally safe/unsafe.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a security expert providing detailed comparative analysis."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=700
    )

    return response['choices'][0]['message']['content']


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if url is not None:
            # Single website analysis
            chatgpt_analysis, results = analysis(url)
            return render_template("results.html", url=url, results=results, chatgpt_analysis=chatgpt_analysis)
        else:
            # Comparative analysis for two websites
            url1 = request.form.get("url-1")
            url2 = request.form.get("url-2")

            url1_analysis, results1 = analysis(url1)
            url2_analysis, results2 = analysis(url2)

            # Generate comparative analysis
            chatgpt_comparative_analysis = comparitive_analysis(url1_analysis, url2_analysis, results1, results2)

            return render_template(
                "results.html",
                url1=url1,
                url2=url2,
                results1=results1,
                results2=results2,
                chatgpt_analysis=chatgpt_comparative_analysis
            )

    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)
