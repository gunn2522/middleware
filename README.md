# 🛠️ ERP Middleware Automation for Frappe/ERPNext

This project is a Django-based middleware automation system that integrates with **Frappe/ERPNext** to streamline Sales Order creation, Payment Entry, and other ERP workflows. It reduces manual work through role-based approvals and automatic document generation.

---

## 🚀 Features

- 📦 **Automated Sales Order Submission**
- 💰 **Automatic Payment Entry Creation**
- 👤 **Role-Based Approval Workflows**
- 🔗 **Real-Time ERP Integration (Frappe API)**
- 📋 **Planned: Stock Entry Automation**
- 🔐 **Environment-based Configuration using `.env`**

---

## 📁 Project Structure

middleware/
├── .idea/ # IDE configurations
├── erp_integration/ # ERP API integration logic
├── erp_middle/ # Core middleware logic
├── orders/ # Sales order and request handling
├── users/ # User management and roles
├── db.sqlite3 # Local development database
├── db.sql # SQL dump for initial setup
├── .env # Environment variables (DO NOT SHARE)
├── .gitignore # Git ignored files
├── manage.py # Django management script


## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/middleware.git
cd middleware


2. Install Requirements
pip install -r requirements.txt

3. Configure Environment Variables
Create a .env file and add your credentials:
ERP_API_KEY=your_erp_api_key
ERP_API_SECRET=your_erp_api_secret
ERP_BASE_URL=https://your-erp-url.com

4. Run the Django Server
python manage.py runserver

✅ Workflow Overview
A user (e.g., delivery boy) submits a request.

Warehouse manager or approver reviews and approves it.

Middleware automatically:

Creates a Sales Order

Links a Payment Entry

(Upcoming) Creates a Stock Entry

Changes are synced to the ERP system in real-time.


🧰 Tech Stack
Backend: Python, Django

Database: SQLite

ERP Platform: Frappe / ERPNext

APIs: Frappe REST API

Env Management: python-dotenv

📌 Roadmap
 Sales Order Auto-Submission

 Payment Entry Automation

 Stock Entry Post Approval

 ERP Exception Handling

 Email Notifications


🤝 Contributing
Contributions, suggestions, and improvements are welcome! Feel free to fork the project, open issues, or submit PRs.


📄 License
This project is licensed under the MIT License.

📬 Contact
Author: Gunn Malhotra
📧 Email: [gunnmlhtr@gmail.com](mailto:gunnmlhtr@gmail.com)


