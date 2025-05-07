from telegram import Bot
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timedelta

load_dotenv()

class TelegramAnalytics:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.channel_username = os.getenv('TELEGRAM_CHANNEL_USERNAME')
        self.bot = None
        if self.bot_token:
            try:
                self.bot = Bot(token=self.bot_token)
            except Exception as e:
                print(f"Warning: Could not initialize Telegram bot: {e}")

    async def get_channel_stats(self):
        if not self.bot:
            return {
                'channel_name': 'Telegram Bot Not Configured',
                'subscribers': 'N/A',
                'description': 'Please set up TELEGRAM_BOT_TOKEN in .env file',
                'messages': []
            }
            
        try:
            # Get channel information
            chat = await self.bot.get_chat(self.channel_username)
            
            # Get recent messages (last 100)
            messages = []
            async for message in self.bot.get_chat_history(chat.id, limit=100):
                messages.append({
                    'date': message.date,
                    'views': message.views if hasattr(message, 'views') else 0,
                    'forwards': message.forward_count if hasattr(message, 'forward_count') else 0
                })

            return {
                'channel_name': chat.title,
                'subscribers': chat.members_count if hasattr(chat, 'members_count') else 'N/A',
                'description': chat.description,
                'messages': messages
            }
        except Exception as e:
            print(f"Error fetching channel stats: {e}")
            return {
                'channel_name': 'Error Fetching Stats',
                'subscribers': 'N/A',
                'description': str(e),
                'messages': []
            }

    def get_stats(self):
        return asyncio.run(self.get_channel_stats()) 