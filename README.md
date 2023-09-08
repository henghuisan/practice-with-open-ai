<h1 align="center" id="title">Practice with Open AI Platform </h1>

An implementation of AI tools including image and essay generator, speech to text, AI chatbot via API of Open AI Platform

## Table of Contents

[🚀 Demo](#demo) <br />
[💻 Project Overview](#getting-started) <br />
[🛠️ Installation](#installation) <br />
[☎️ Contact](#contact) <br />

## 🚀 Demo
[Practice with Open AI platform](https://practice-with-open-ai.vercel.app/)

## 💻 Project Overview
On the website, you can access four distinct functionalities:

- AI Chatbot
- Image Generator
- Essay Generator
- Speech To Text Conversion

## 🛠️ Installation
### 1. Prerequisites
Before you begin, ensure you have the following requirements in place:

- **Python**: Install Python from the [Python website](https://www.python.org/downloads/).

- **Open AI**: Create account from [Open AI](https://openai.com/).

- **Cloudinary**: Create account from [Cloudinary](https://cloudinary.com/).

### 2. Clone the Repository
Clone this repository to your local machine using:

```bash
git clone https://github.com/henghuisan/practice-with-open-ai.git
```
### 3. Create a Virtual Environment
Navigate to the cloned directory:

``` bash
cd practice-with-open-ai
```

Create a virtual environment:

- On macOS and Linux:
``` bash
python3 -m venv venv
source venv/bin/activate
```

- On Windows:
``` bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```

### 5. Create a `.env` File
In the root directory of the project, create a file named `.env`.

### 6. Define Environment Variables
Inside the `.env` file, define the necessary environment variables using the following format:

```plaintext
FLASK_APP=app.py
FLASK_ENV=development
OPENAI_API_KEY=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

### 7. Create Open AI Key

Go to [this page](https://platform.openai.com/account/api-keys) to create your API key and assign the key to the `OPENAI_API_KEY` variable in your `.env` file.

### 8. Cloudinary Setup
Go to [this page](https://console.cloudinary.com/console/c-c74771f54ad46e333740e0fb85b24c/getting-started) to copy the snippets for your Cloudinary environment variables.

### 9. Run the Development Server
Start the development server and run the app:
```bash
flask run
```

You should now be able to access the app http://localhost:5000/

## ☎️ Contact

For questions or feedback, feel free to reach out:

- Email: gracehenghuisan@gmail.com
