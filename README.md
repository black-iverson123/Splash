# Splash

Splash is a Flask-based web application that provides a platform for managing communities, real-time chat, cryptocurrency data, and more. This project integrates various features such as user authentication, community management, and external API integration.

---

## Features

- **User Authentication**: Secure login, registration, and account management.
- **Community Management**: Create, join, and interact with communities.
- **Real-Time Chat**: Chat functionality powered by Flask-SocketIO.
- **Cryptocurrency Data**: Fetch and display cryptocurrency data using the CoinMarketCap API.
- **Dark Mode**: Toggle between light and dark themes.
- **Search Functionality**: Search for users and communities.

---

## Technologies Used

- **Backend**: Flask, Flask-SocketIO, Flask-Mail, Flask-WTF
- **Frontend**: HTML, CSS, Bootstrap, JavaScript (jQuery)
- **Database**: SQLAlchemy
- **APIs**: CoinMarketCap API
- **Other Tools**: Flask-Migrate, Flask-Login, Flask-Moment

---

## Installation

### Prerequisites
- Python 3.10 or higher
- Virtual environment (optional but recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/splash.git
   cd splash
2. Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
    pip install -r requirements.txt
4. Set up environment variables
    create a .env file in root directory
    contents:
    SECRET_KEY=your_secret_key
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=587 or 465
    MAIL_USE_TLS or SSL=True 
    MAIL_USERNAME=your_email@example.com
    MAIL_PASSWORD=your_email_password
    API_KEY=your_coinmarketcap_api_key
    # Database configuration
    DATABASE_URL="sqlite:///splash.db"
    SQLALCHEMY_TRACK_MODIFICATIONS="False"

5  Run the application
    flask run

# Usage
Real-Time Chat
    **Join a community to access the chat room.**
    **Send and receive messages in real time.**
Cryptocurrency Data
    **View the latest cryptocurrency data fetched from the CoinMarketCap API.**
    **Search for specific cryptocurrencies by symbol.**
Dark Mode
    **Toggle between light and dark themes using the dark mode button.**

#Contributing
Contributions are most welcome!!, Please follow this steps:
1. Fork the repo
2. create a new branch
    checkout -b feature-name
3. Commit your changes:
    git commit -m "Added feature-name"
4. Push to the branch
    git push origin feature-name
5. Open a pull request

# License
This project is licensed under the MIT License. See the LICENSE file for details.
