# **Finance telegram bot**

This application will help you and your family to effectively monitor their finances and manage them properly
## Getting started locally
1. Clone project
    ```cmd
    git clone https://github.com/Vitaliy985/TelegramBot.git 
   ```
2. Install dependencies
    ```cmd
   python install -r requirements.txt
   ```
3. Database connection. Create config.json:
    ```json
   {
      "Token": "YOUR TELEGRAM TOKEN",
      "ConnectionString":
           {
              "host": "YOUR HOST",
              "user": "YOUR USER",
              "password": "YOUR PASSWORD",
              "database": "YOUR DATABASE NAME"
           }
   }
   ```
4. Run the bot
    ```cmd
    python .\TelegramBot\main.py
    ```
5. Generate docs (html):
   ```cmd
   cd docs
   make.bat html
   ```
## Getting started with docker
1. Add .env file
2. Build and run containers
    ```cmd
    docker compose --env-file .env up --build
    ```
 3. In bot container add migrations
    ```cmd
    alembic upgrade head
    ```
## [See documentation here](https://vitaliy985.github.io/TelegramBot/)
