# Discord Server Stats Bot

This Discord bot creates a category called **Server Stats** with 4 voice channels displaying:  
- Members: [member count]  
- Bots: [bot count]  
- Roles: [role count]  
- Version [version]

Each voice channel is visible to everyone but no one can connect to them.

---

## Setup

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Install dependencies:

    ```bash
    pip install -U discord.py aiohttp
    ```

3. Replace the bot token:

    - Open `main.py`.
    - Replace `"YOUR_BOT_TOKEN"` with your Discord bot token.

    > **Important:** Keep your bot token secret! Do **not** share it publicly.

4. Run the bot:

    ```bash
    python main.py
    ```

---

## How it works

- On startup, the bot checks if the **Server Stats** category and the 4 voice channels exist.  
- If any are missing, it creates them.  
- Channels update their counts based on the current guild info on bot restart.  
- Members, bots, and roles channels update live on user join, bot join, and role creation respectively.  
- Version channel checks GitHub every 30 minutes to update the version number.

---

## Commands

Each voice channel creation is handled by its own cog on startup. You can add commands if needed.

---

## License

MIT License (or your preferred license)
