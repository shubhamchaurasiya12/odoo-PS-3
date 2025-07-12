# ReWear – Community Clothing Exchange Web App

## 💡 Overview
ReWear is a responsive web platform that enables users to exchange unused clothes with other community members through direct swaps. The platform encourages sustainable fashion and helps reduce textile waste.

---

## 🧪 Tech Stack
- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** MongoDB (via PyMongo)
- **Other:** Jinja2, Werkzeug, python-dotenv

---

## 🎯 Features
- User registration and login (with secure password hashing)
- User dashboard with profile, uploaded items, and swap history
- Upload new clothing items with images and details
- Browse available items and view item details
- Request swaps with other users
- Admin panel for approving/rejecting items and managing users
- Responsive, modern UI with Bootstrap and custom CSS

---

## 📁 Project Structure
```
ReWear/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── base.html, home.html, login.html, register.html, dashboard.html, ...
│
├── static/
│   ├── css/
│   │   ├── login.css, style.css
│   ├── js/
│   │   ├── login.js, script.js
│   └── Images/
│
├── models/
│   ├── __init__.py, db.py
│
├── auth/
│   ├── __init__.py, routes.py, utils.py
│
├── items/
│   ├── __init__.py, routes.py
│
└── admin/
    ├── __init__.py, routes.py
```

---

## 🚀 Getting Started

### 1. **Clone the repository**
```sh
git clone <your-repo-url>
cd ReWear
```

### 2. **Create a virtual environment**
- **Windows:**
  ```sh
  python -m venv venv
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```sh
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. **Install dependencies**
```sh
pip install -r requirements.txt
```

### 4. **Set up environment variables**
Create a `.env` file in the project root:
```
SECRET_KEY=your_secret_key_here
MONGODB_URI=your_mongodb_connection_string
```

### 5. **Run the app**
```sh
python app.py
```
Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🛠️ Customization
- Update logo and images in `static/Images/`
- Adjust styles in `static/css/login.css` and `static/css/style.css`
- Edit templates in the `templates/` folder

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
This project is licensed under the MIT License. 
