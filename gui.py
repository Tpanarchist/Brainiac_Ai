import tkinter as tk
from tkinter import scrolledtext
import threading
import requests
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ChatWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Brainiac Chat Interface")

        self.chat_history = scrolledtext.ScrolledText(root, state='disabled', height=20, width=70)
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.grid(row=1, column=0, padx=10, sticky="ew")

        self.send_button = tk.Button(root, text="Send", command=self.send_message_to_backend)
        self.send_button.grid(row=1, column=1, padx=10, sticky="ew")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Define the API URL for local hosting
        self.api_url = "http://127.0.0.1:9000/message"

        # Start a thread to periodically poll for new messages
        self.polling_thread = threading.Thread(target=self.poll_for_new_messages, daemon=True)
        self.polling_thread.start()

    def send_message_to_backend(self):
        message = self.message_entry.get()
        if message:
            try:
                logging.info(f"Sending message to backend: {message}")
                # Adjusted to send message to bus=north and layer=0 for the Aspirational Layer to process
                response = requests.post(self.api_url, json={"message": message, "bus": "north", "layer": 0})
                if response.status_code == 200:
                    self.display_message(f"You: {message}", "right")
                    self.message_entry.delete(0, tk.END)
                    logging.info("Message sent successfully.")
                else:
                    logging.error(f"Failed to send message, status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Error sending message to backend: {e}")

    def display_message(self, message, alignment="left"):
        self.chat_history.config(state='normal')
        if alignment == "right":
            self.chat_history.tag_configure("right", justify='right')
            self.chat_history.insert(tk.END, message + "\n", "right")
        else:
            self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.config(state='disabled')
        self.chat_history.yview(tk.END)

    def poll_for_new_messages(self):
        while True:
            try:
                logging.info("Polling for new messages.")
                # Polling for new messages from layer 1 where the Aspirational Layer sends its responses
                response = requests.get(self.api_url, params={"bus": "north", "layer": 1})
                if response.status_code == 200:
                    messages = response.json().get('messages', [])
                    for message in messages:
                        self.display_message(f"Brainiac: {message['message']}")
                        logging.info(f"Received message: {message['message']}")
                else:
                    logging.error(f"Polling failed, status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Error polling for new messages: {e}")
            time.sleep(5)  # Poll every 5 seconds without using root.after in a thread

if __name__ == "__main__":
    root = tk.Tk()
    chat_window = ChatWindow(root)
    root.mainloop()
