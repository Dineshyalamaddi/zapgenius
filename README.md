# ZapGenius

ZapGenius is an AI-powered automation recommender that suggests useful Zaps (workflows) based on user activity.  
It analyzes repetitive actions and provides intelligent recommendations to save time and improve productivity.  

---

## 🚀 Features
- Embedding-based similarity model for recommending Zaps.  
- Rule-based fallback recommender.  
- Streamlit interface for user interaction.  
- Works with sample user activity data.  

---

## 📂 Project Structure
zapgenius/
│── data/
│ └── sample_user_data.json # Example user activity data
│── src/
│ ├── embedding_model.py # Embedding model for text similarity
│ ├── recommender.py # Rule-based + embedding-based recommender
│── zapgenius_demo.ipynb # Jupyter notebook demo
│── zapgenius_demo.py # Streamlit app entry point
│── requirements.txt # Project dependencies
│── README.md # Project documentation

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dineshyalamaddi/zapgenius.git
   cd zapgenius

2. Install dependencies

pip install -r requirements.txt

3. Run the Streamlit app

streamlit run zapgenius_demo.py

🧪 Usage

The app will load sample_user_data.json.

Enter a description of your workflow.

The recommender suggests the top 5 Zaps with similarity scores.

📌 Example

Input:

Send new Gmail attachments to Google Drive

Output:

1. Save Gmail attachments to Google Drive (Score: 0.92)
2. Backup Gmail files into Dropbox (Score: 0.88)
3. Save new email files into OneDrive (Score: 0.84)
...


🛠️ Requirements

Python 3.8+
Streamlit
Scikit-learn
Pandas
NumPy

👨‍💻 Author  

Dinesh Yalamaddi  


