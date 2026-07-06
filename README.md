<div align="center">

<a href="https://github.com/Suman18-bit/DEPLOY_REPO">
  <img src="./header-animation.svg" alt="AskMyBook Animated Banner" width="100%">
</a>
</div>
<div align="center">

<a href="https://github.com/Suman18-bit/DEPLOY_REPO">
  <img src="https://readme-typing-svg.herokuapp.com/?font=Fira+Code&weight=600&size=30&pause=1000&color=3776AB&center=true&vCenter=true&width=600&height=80&lines=Welcome+to+DEPLOY_REPO+🚀;Retrieval-Augmented+Generation+Engine;Seamlessly+Deployed+on+Vercel!;Powered+by+Python+🐍" alt="Typing SVG" />
</a>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Vercel">
  <img src="https://img.shields.io/github/license/Suman18-bit/DEPLOY_REPO?style=for-the-badge&color=green" alt="License">
  <img src="https://img.shields.io/github/last-commit/Suman18-bit/DEPLOY_REPO?style=for-the-badge&color=blue" alt="Last Commit">
</p>

<img src="https://cdn.dribbble.com/users/1162077/screenshots/3848914/programmer.gif" width="400" alt="Animated coding gif">

<p align="center">
  <strong>An intelligent web application featuring Document Processing and a RAG (Retrieval-Augmented Generation) Engine.</strong>
</p>

</div>

---

## ✨ Features

- 🧠 **RAG Engine:** Intelligent retrieval-augmented generation using `rag_engine.py`.
- 📄 **Document Processing:** Automated document parsing and handling via `document_processor.py`.
- ⚡ **Serverless Deployment:** Fully optimized for Vercel deployment with automated setup scripts.
- 🎨 **Web Interface:** Front-end templates and static assets ready to go.

---

## 📂 Repository Structure

```graphql
📦 DEPLOY_REPO
 ┣ 📂 db                    # Database storage/configuration
 ┣ 📂 public/data           # Publicly accessible data files
 ┣ 📂 static                # CSS, JS, and static assets
 ┃ ┣ 📂 css
 ┃ ┗ 📂 js
 ┣ 📂 templates             # HTML Web Templates
 ┣ 📜 app.py                # Main Application Entry Point
 ┣ 📜 rag_engine.py         # Core RAG implementation logic
 ┣ 📜 document_processor.py # Document parsing and extraction
 ┣ 📜 setup_vercel.py       # Deployment setup script
 ┣ 📜 vercel.json           # Vercel serverless configuration
 ┣ 📜 requirements.txt      # Python dependencies
 ┗ 📜 LICENSE               # Open-source license

```

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### 1. Clone the repository

```bash
git clone [https://github.com/Suman18-bit/DEPLOY_REPO.git](https://github.com/Suman18-bit/DEPLOY_REPO.git)
cd DEPLOY_REPO

```

### 2. Set up a virtual environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```

### 3. Install dependencies

```bash
pip install -r requirements.txt

```

### 4. Environment Variables

Create a `.env` file in the root directory and add your required API keys and database URIs.

```env
# Example .env file
OPENAI_API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here

```

### 5. Run the application

```bash
python app.py

```

*Navigate to `http://localhost:5000` (or your configured port) in your browser.*

---

## 🌐 Deployment

This project is configured for seamless deployment on **Vercel**.

1. Ensure the Vercel CLI is installed.
2. The `vercel.json` and `setup_vercel.py` handle the necessary build steps and serverless function configurations.
3. Simply run `vercel` in your terminal or link the repository to your Vercel dashboard.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://www.google.com/search?q=https://github.com/Suman18-bit/DEPLOY_REPO/issues).
