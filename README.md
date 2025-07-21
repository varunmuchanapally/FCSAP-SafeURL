# FCSAP-SafeURL


Here’s a professional `README.md` for your **SafeURL: URL Safety Checker** Flask app. This includes sections for features, setup instructions, API keys, and usage.

---

````markdown
 SafeURL: URL Safety Checker

SafeURL is a Flask-based web application that analyzes the safety of a given website using multiple techniques such as:

- HTTPS validation
- SSL/TLS certificate verification
- IP and geolocation lookup
- Google Safe Browsing API for reputation
- Optional domain age check (via WHOIS API)
- GPT-4o-powered safety analysis and comparative assessments


 🚀 Features

✅ Single or Comparative website analysis  
✅ Real-time HTTPS and certificate verification  
✅ IP and geolocation tracking (via IPStack)  
✅ Google Safe Browsing for malicious URL detection  
✅ Professional summary using GPT-4o (OpenAI)  
✅ Clean, mobile-friendly UI



⚙️ Setup Instructions
1. Clone the Repository

git clone https://github.com/yourusername/safeurl-checker.git
cd safeurl-checker

2. Create & Activate Environment

bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate


3. Install Dependencies

bash
pip install -r requirements.txt


4. Add Your API Keys

In `app.py`, replace the placeholders with your actual API keys:

openai.api_key = "YOUR_OPENAI_API_KEY"
api_key = "YOUR_IPSTACK_API_KEY"
key = "YOUR_GOOGLE_SAFE_BROWSING_API_KEY"

5. Run the App

bash
python app.py


Then go to `http://127.0.0.1:5000` in your browser.



🧠 Analysis Powered by OpenAI GPT-4o

SafeURL leverages OpenAI’s GPT-4o to produce:

* Detailed 250-word assessments per URL
* Clear Safe/Unsafe decisions
* Comparative summaries of two websites



📁 Project Structure


safeurl-checker/
│
├── templates/
│   ├── index.html
│   └── results.html
│
├── static/
│   └── styles.css
│
├── app.py
├── README.md
└── requirements.txt




🔐 API Keys Required

| Service                  | Use Case                      | Source                                                                                                                   |
| ------------------------ | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| OpenAI GPT-4o            | Website safety analysis       | [https://platform.openai.com/](https://platform.openai.com/)                                                             |
| Google Safe Browsing API | URL reputation check          | [https://developers.google.com/safe-browsing/v4/get-started](https://developers.google.com/safe-browsing/v4/get-started) |
| IPStack API              | IP geolocation data           | [https://ipstack.com/](https://ipstack.com/)                                                                             |
| WhoisXML API (Optional)  | Domain creation date analysis | [https://whois.whoisxmlapi.com/](https://whois.whoisxmlapi.com/)                                                         |



📦 Dependencies

List of important packages:

* Flask
* Requests
* OpenAI
* socket / ssl / urllib
* PyOpenSSL (if used)









📃 License

[MIT License](LICENSE)





![WhatsApp Image 2024-11-20 at 1 22 43 PM](https://github.com/user-attachments/assets/8c7f8cf0-e1f4-4687-aa99-1ec25e1855d3)
![WhatsApp Image 2024-11-20 at 1 23 00 PM](https://github.com/user-attachments/assets/6b64d57e-b52c-4303-9b46-86bc46ad3321)
![WhatsApp Image 2024-11-20 at 1 27 50 PM](https://github.com/user-attachments/assets/1558e970-500f-4a04-97a9-a0994d740ecd)
![WhatsApp Image 2024-11-20 at 1 23 59 PM](https://github.com/user-attachments/assets/91aa8f15-ddd5-4bcd-8248-f25333caeea7)
![WhatsApp Image 2024-11-20 at 1 24 12 PM](https://github.com/user-attachments/assets/6b718b34-c8ab-46d5-a9f4-442a96acec9a)
![WhatsApp Image 2024-11-20 at 1 25 06 PM](https://github.com/user-attachments/assets/971ba87f-6eed-4244-bbe1-c637b9b96d51)
![WhatsApp Image 2024-11-20 at 1 26 19 PM](https://github.com/user-attachments/assets/e4941b21-921b-4061-9821-76e5ee37a381)
![WhatsApp Image 2024-11-20 at 1 26 51 PM](https://github.com/user-attachments/assets/5c25c5f8-d697-4bf5-b09a-da504397fe16)
![WhatsApp Image 2024-11-20 at 1 27 31 PM](https://github.com/user-attachments/assets/396a3aac-dd7f-4ce3-b8e2-aa68273d669c)




