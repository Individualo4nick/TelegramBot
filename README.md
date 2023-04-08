# **Finance telegram bot**

This application will help you and your family to effectively monitor their finances and manage them properly
## Getting started
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
## [See documentation here](./docs/_build/html/index.html)