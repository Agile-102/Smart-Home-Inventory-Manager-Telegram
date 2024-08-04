# Smart Home Inventory Manager for Telegram

This repository is for the Smart Home Inventory Manager Telegram Bot. Deployed on Render.

## Telegram
Find the Bot on Telegram! [@SHIM_Tele_Bot](https://t.me/SHIM_Tele_Bot)

## Commands

* `/start` - Initiate contact with SHIM Bot.
* `/help` - View available functions.
* `/add_room` - Add a new room.
* `/add_subspace` - Add a new sub-space.
  
<!--
* `/additem` - Add a new item.
* `/view` - View all spaces and sub-spaces.
* `/delete` - Delete a space or sub-space by ID.
* `/remove_item` - Remove an item by ID.
 -->

## Working on this Repo
1. Copy the repo into your working dir to get started
    ```sh
    git clone https://github.com/Agile-102/Smart-Home-Inventory-Manager-Telegram.git
    ```
2. Make sure to install the required packages:
    ```
    pip install python-telegram-bot requests
    ```
3. Logic engine (spaCy) installation:
   ```
    pip install spacy
    python -m spacy download en_core_web_sm
    ```
4. Make sure to update and track changes before adding, commiting and pushing to repo with:
   ```
    git pull
    ```

## Running the Bot
Run the script with the following command:
```
python SHIM_tele_bot.PY
```


## About Render Free Usage

Render spins down a Free web service that goes 15 minutes without receiving inbound traffic. Render spins the service back up whenever it next receives a request to process.

Spinning up a service takes up to a minute, which causes a noticeable delay for incoming requests until the service is back up and running. For example, a browser page load will hang temporarily.

More information on usage limits such as outbound bandwidth and build pipeline minutes available at: https://docs.render.com/free

## About Logic Engine: spaCy

spaCy is a free, open-source library for advanced Natural Language Processing (NLP) in Python. It’s designed specifically for production use and helps you build applications that process and “understand” large volumes of text. It can be used to build information extraction or natural language understanding systems.

More information on spaCy available at: https://spacy.io/
spaCy API Docs: https://spacy.io/api