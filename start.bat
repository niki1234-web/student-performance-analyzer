@echo off 
cd /d "C:\Users\R.C.V\Downloads\student-performance-analyzer\student-performance-analyzer" 
set MONGODB_URI=mongodb+srv://prajapatinikita052_db_user:MongoDbPass7506@cluster0.doc3cys.mongodb.net/?appName=Cluster0 
start "Ngrok Tunnel" cmd /k "ngrok http --url=purify-feel-cartridge.ngrok-free.dev 8501" 
python -m streamlit run app.py
