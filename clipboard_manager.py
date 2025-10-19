import rumps
import pyperclip
import time
import threading
import json
import os

class ClipboardApp(rumps.App):
    def __init__(self):
        super(ClipboardApp, self).__init__("Clipboard", quit_button=None)
        self.max_items = 20
        self.last_text = ""
        self.json_path = os.path.join(os.path.dirname(__file__), "clipboard.json")
        self.history = self.load_history()
        self.update_menu()
        thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        thread.start()

    def load_history(self):
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data[: self.max_items]
            except Exception as e:
                print(f"Error loading clipboard.json: {e}")
        return []

    def save_history(self):
        try:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(self.history[: self.max_items], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving clipboard.json: {e}")

    def monitor_clipboard(self):
        while True:
            try:
                text = pyperclip.paste()
                if text and text != self.last_text:
                    self.last_text = text
                    if text not in self.history:
                        self.history.insert(0, text)
                        if len(self.history) > self.max_items:
                            self.history = self.history[: self.max_items]
                        self.save_history()
                        # update menu on main thread — rumps is simple enough to allow this call
                        self.update_menu()
            except Exception as e:
                print(f"Error accessing clipboard: {e}")
            time.sleep(1)

    def update_menu(self):
        items = []
        if not self.history:
            items.append(rumps.MenuItem("No items yet", None))
        else:
            for text in self.history:
                title = text[:60].replace("\n", " ") + ("..." if len(text) > 60 else "")
                item = rumps.MenuItem(title, callback=self.copy_item)
                item.value = text  # store full text
                items.append(item)
            items.append(None)  # separator
        items.append(rumps.MenuItem("Clear History", callback=self.clear_history))
        items.append(rumps.MenuItem("Quit", callback=self.quit_app))
        self.menu = items

    def copy_item(self, sender):
        # Copy the full text, not the truncated title
        try:
            pyperclip.copy(sender.value)
            rumps.notification("Clipboard Manager", "Copied to Clipboard", sender.value[:60])
        except Exception as e:
            print(f"Error copying to clipboard: {e}")

    def clear_history(self, sender):
        self.history = []
        self.save_history()
        self.update_menu()

    def quit_app(self, sender):
        rumps.quit_application()

if __name__ == "__main__":
    json_path = os.path.join(os.path.dirname(__file__), "clipboard.json")
    if not os.path.exists(json_path):
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error creating clipboard.json: {e}")
    app = ClipboardApp()
    app.run()