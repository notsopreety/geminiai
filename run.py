import asyncio
import aiohttp
import uuid
import sys
import os
from urllib.parse import quote
from datetime import datetime

class ANSIColors:
    """Native ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Foreground Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Background Colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

class AIAssistant:
    def __init__(self, api_url: str):
        self.API_URL = api_url
        self.conversations = {}
        self.current_user_id = None
        self.system_prompt = "You are a helpful, friendly AI assistant named Ace. Provide concise and accurate responses."

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        """Display ASCII art banner with native colors."""
        current_time = datetime.now().strftime("%A - %d{suffix} %B, %Y [%H:%M:%S]")
        day = int(datetime.now().strftime("%d"))
        if 11 <= day <= 13:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        
        formatted_time = current_time.replace("{suffix}", suffix)

        banner = f"""{ANSIColors.CYAN}
  ██████╗ ███████╗███╗   ███╗██╗███╗   ██╗██╗
 ██╔════╝ ██╔════╝████╗ ████║██║████╗  ██║██║
 ██║  ███╗█████╗  ██╔████╔██║██║██╔██╗ ██║██║
 ██║   ██║██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║╚═╝
 ╚██████╔╝███████╗██║ ╚═╝ ██║██║██║ ╚████║██╗
  ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝ -By Samir Thakuri
{ANSIColors.RESET}
{ANSIColors.YELLOW}Current Time: {formatted_time}{ANSIColors.RESET}
"""
        print(banner)
        print(f"{ANSIColors.GREEN}=" * 50)
        print(f"{ANSIColors.YELLOW}Welcome to the Advanced AI Assistant CLI!{ANSIColors.RESET}")
        print(f"{ANSIColors.GREEN}=" * 50)

    def print_help(self):
        """Display help commands with native colors."""
        print(f"{ANSIColors.MAGENTA}Available Commands:{ANSIColors.RESET}")
        print(f"{ANSIColors.BLUE}  /new    - Start a new chat session{ANSIColors.RESET}")
        print(f"{ANSIColors.BLUE}  /system - Change system prompt{ANSIColors.RESET}")
        print(f"{ANSIColors.BLUE}  /clear  - Clear screen and reset interface{ANSIColors.RESET}")
        print(f"{ANSIColors.BLUE}  /exit   - Exit the application{ANSIColors.RESET}")
        print(f"{ANSIColors.GREEN}=" * 50)

    def generate_user_id(self):
        """Generate a new unique user ID."""
        return str(uuid.uuid4())

    async def stream_text(self, text: str, delay: float = 0.01):
        """Stream text output with a faster typing effect."""
        for char in text:
            print(f"{ANSIColors.WHITE}{char}", end='', flush=True)
            await asyncio.sleep(delay)
        print(ANSIColors.RESET)  # Reset color after streaming

    async def query_ai(self, question: str, user_id: str) -> str:
        """Query custom AI API."""
        try:
            # URL encode the parameters
            encoded_prompt = quote(question)
            encoded_system = quote(self.system_prompt)
            encoded_uid = quote(user_id)

            # Construct the full URL
            full_url = self.API_URL.format(
                prompt=encoded_prompt, 
                sysprompt=encoded_system, 
                uid=encoded_uid
            )

            async with aiohttp.ClientSession() as session:
                async with session.get(full_url) as response:
                    if response.status != 200:
                        return f"Error: {response.status}"
                    
                    response_data = await response.json()
                    return response_data['candidates'][0]['content']['parts'][0]['text'].strip()

        except Exception as e:
            return f"An error occurred: {str(e)}"

    async def cli_chat(self):
        """Interactive CLI chat interface."""
        # Clear screen and show initial banner
        self.clear_screen()
        self.print_banner()
        self.print_help()

        # Initialize first user
        self.current_user_id = self.generate_user_id()
        print(f"{ANSIColors.CYAN}[New Chat Session: {self.current_user_id[:8]}]{ANSIColors.RESET}")
        print(f"{ANSIColors.GREEN}AI Assistant:{ANSIColors.WHITE} Hello! I'm ready to help. What would you like to discuss?{ANSIColors.RESET}")

        while True:
            try:
                user_input = input(f"{ANSIColors.YELLOW}You: {ANSIColors.RESET}").strip()

                if user_input.lower() == '/exit':
                    print(f"{ANSIColors.GREEN}\nGoodbye! 👋{ANSIColors.RESET}")
                    break
                
                elif user_input.lower() == '/new':
                    # Confirm starting a new chat
                    confirm = input(f"{ANSIColors.MAGENTA}Start a new chat session? (Y/n): {ANSIColors.RESET}").lower()
                    if confirm in ['', 'y', 'yes']:
                        # Clear screen and generate new user ID
                        self.clear_screen()
                        self.print_banner()
                        self.print_help()
                        self.current_user_id = self.generate_user_id()
                        print(f"{ANSIColors.CYAN}[New Chat Session: {self.current_user_id[:8]}]{ANSIColors.RESET}")
                        print(f"{ANSIColors.GREEN}AI Assistant:{ANSIColors.WHITE} Fresh chat started! How can I help you today?{ANSIColors.RESET}")
                    continue
                
                elif user_input.lower() == '/clear':
                    # Clear screen with option to change session
                    confirm = input(f"{ANSIColors.MAGENTA}Do you want to start a new chat session? (y/N): {ANSIColors.RESET}").lower()
                    if confirm in ['y', 'yes']:
                        # Clear screen and generate new user ID
                        self.clear_screen()
                        self.print_banner()
                        self.print_help()
                        self.current_user_id = self.generate_user_id()
                        print(f"{ANSIColors.CYAN}[New Chat Session: {self.current_user_id[:8]}]{ANSIColors.RESET}")
                        print(f"{ANSIColors.GREEN}AI Assistant:{ANSIColors.WHITE} Fresh chat started! How can I help you today?{ANSIColors.RESET}")
                    else:
                        # Just clear screen and show existing session
                        self.clear_screen()
                        self.print_banner()
                        self.print_help()
                        print(f"{ANSIColors.CYAN}[Existing Chat Session: {self.current_user_id[:8]}]{ANSIColors.RESET}")
                    continue
                
                elif user_input.lower() == '/system':
                    # Allow changing system prompt
                    new_system_prompt = input(f"{ANSIColors.MAGENTA}Enter new system prompt: {ANSIColors.RESET}").strip()
                    if new_system_prompt:
                        # Ask if user wants to change chat or continue
                        confirm = input(f"{ANSIColors.MAGENTA}Do you want to continue with the current chat session? (Y/n): {ANSIColors.RESET}").lower()
                        if confirm in ['', 'y', 'yes']:
                            self.system_prompt = new_system_prompt
                            print(f"{ANSIColors.GREEN}System prompt updated successfully.{ANSIColors.RESET}")
                        else:
                            # Clear screen and generate new user ID
                            self.clear_screen()
                            self.print_banner()
                            self.print_help()
                            self.current_user_id = self.generate_user_id()
                            self.system_prompt = new_system_prompt
                            print(f"{ANSIColors.CYAN}[New Chat Session: {self.current_user_id[:8]}]{ANSIColors.RESET}")
                            print(f"{ANSIColors.GREEN}AI Assistant:{ANSIColors.WHITE} Fresh chat started with new system prompt!{ANSIColors.RESET}")
                    continue

                print(f"{ANSIColors.GREEN}AI Assistant: {ANSIColors.RESET}", end='', flush=True)
                response = await self.query_ai(user_input, self.current_user_id)
                await self.stream_text(response)

            except KeyboardInterrupt:
                print(f"{ANSIColors.RED}\n\nChat interrupted. Type /exit to quit.{ANSIColors.RESET}")
            except Exception as e:
                print(f"{ANSIColors.RED}\nAn unexpected error occurred: {e}{ANSIColors.RESET}")

def main():
    # Custom API endpoint
    API_URL = "https://www.samirxpikachu.run.place/gemini?text={prompt}&system={sysprompt}&uid={uid}"
    
    assistant = AIAssistant(API_URL)
    asyncio.run(assistant.cli_chat())

if __name__ == "__main__":
    main()