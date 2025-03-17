AI Sports Highlights Generator

The AI Sports Highlights Generator is an intelligent system that leverages computer vision and machine learning to automatically detect and extract highlights from sports videos. It combines YOLO (You Only Look Once) for real-time object detection with a Streamlit-powered backend and an Angular frontend for a modern, user-friendly interface.

✨ Features
🎯 Automatic Highlight Detection using YOLO
⚽ Support for Multiple Sports (e.g., football, basketball, etc.)
⚡ Real-time Processing
🌐 Web-based UI powered by Streamlit and Angular
🗃️ Easy to Deploy and extendable for additional sports and features
🛠️ Installation & Setup
1️⃣ Backend (Streamlit + YOLO)
Clone this repository:

bash
Copy code
git clone https://github.com/your-username/ai-sports-highlights-generator.git
cd ai-sports-highlights-generator
Install backend dependencies:

bash
Copy code
pip install -r requirements.txt
Run the backend (Streamlit app):

bash
Copy code
streamlit run backend/app.py
2️⃣ Frontend (Angular)
Navigate to the frontend directory:

bash
Copy code
cd frontend
If needed, initialize a new Angular project:

bash
Copy code
npx @angular/cli@16 new frontend --skip-git --skip-tests --style=scss --routing
Move your existing frontend files into the newly created Angular project structure (e.g., into /src/app and /src/assets).

Install frontend dependencies:

bash
Copy code
npm install
Start the frontend dev server:

bash
Copy code
ng serve
🚀 Deployment
Local Deployment: The backend will run on http://localhost:8501 (Streamlit), and the Angular frontend will be available on http://localhost:4200.

Production Deployment:

Deploy Streamlit backend to services like Streamlit Cloud, Heroku, or AWS EC2.
Build Angular for production:
bash
Copy code
ng build --prod
Then serve it via NGINX, Netlify, or Vercel.
🗂️ Project Structure
graphql
Copy code
ai-sports-highlights-generator/
│
├── backend/
│   ├── app.py               # Streamlit main app
│   ├── yolo/                # YOLO models and config
│   ├── utils/               # Helper functions
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── src/
│   ├── angular.json
│   └── package.json         # Angular dependencies
│
├── README.md
└── .gitignore
📢 Notes
Ensure YOLO model weights are downloaded and placed in the correct backend/yolo/ directory.
Customize your highlight logic based on sport-specific rules inside app.py or related modules.
You can connect the backend and frontend using REST API or via websocket if you need real-time interaction.
📸 Demo Screenshot
(Add an image or gif of your app working here once hosted!)

🧑‍💻 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.