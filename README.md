# GeminiAI CLI Assistant

GeminiAI is an interactive CLI-based AI assistant built using Python. It allows users to chat with a custom AI model through a simple and engaging terminal interface. The assistant supports session management, dynamic system prompts, and real-time response streaming.

---

## **Features**
- Interactive CLI for chat-based AI interactions.
- Customizable system prompt for flexible response styles.
- Session management with unique session IDs.
- Clear and colorful terminal outputs.
- Dynamic text streaming for AI responses.

---

## **Installation**
Follow these steps to install and run the script in **Termux**:

1. **Update & Install Python**:
   ```bash
   pkg update -y && pkg upgrade -y
   pkg install python git -y
   ```

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/notsopreety/geminiai.git
   ```

3. **Navigate to the Directory**:
   ```bash
   cd geminiai
   ```

4. **Install Dependencies**:
   Install Python dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

5. **Make the Script Globally Accessible**:
   Create a symbolic link for the script:
   ```bash
   echo "cd $(pwd) && python run.py" > $PREFIX/bin/geminiai
   chmod +x $PREFIX/bin/geminiai
   ```

---

## **Usage**
To start the assistant, simply type the following in your terminal:
```bash
geminiai
```

### **Commands**
- `/new` - Start a new chat session.
- `/system` - Change the system prompt.
- `/clear` - Clear the screen.
- `/exit` - Exit the application.

---

## **Example Interaction**
```plaintext
Welcome to the Advanced AI Assistant CLI!
==================================================
[New Chat Session: 1234abcd]
AI Assistant: Hello! I'm ready to help. What would you like to discuss?

You: What is Python?
AI Assistant: Python is a high-level, interpreted programming language known for its simplicity and versatility.
```

---

## **License**
This project is licensed under the MIT License.

---

## **Credits**
Created by **Samir Thakuri**. <br>
API by **Syed Samir Chowdhury**.
