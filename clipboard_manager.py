import rumps
import pyperclip
import threading
import time
import json
import os


class ClipboardApp(rumps.App):
    def __init__(self):
        super(ClipboardApp, self).__init__("📋", quit_button=None)
        self.menu = ["Clipboard History", None, "Quit"]
        self.max_items = 20
        self.last_text = ""
        self.json_path = os.path.join(os.path.dirname(__file__), "clipboard.json")
        self.data = self.load_data()
        self.history = self.data.get("history", [])
        self.bookmarks = self.data.get("bookmarks", [])
        self.update_menu()

        thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        thread.start()

    def load_data(self):
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    return {"history": data[:self.max_items], "bookmarks": []}
                if isinstance(data, dict):
                    data.setdefault("history", [])
                    data.setdefault("bookmarks", [])
                    return data
            except Exception as e:
                print(f"Error loading clipboard.json: {e}")
        return {"history": [], "bookmarks": []}

    def save_data(self):
        self.data["history"] = self.history[:self.max_items]
        self.data["bookmarks"] = self.bookmarks
        try:
            with open(self.json_path, "w") as f:
                json.dump(self.data, f, indent=2)
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
                        self.save_data()
                        self.update_menu()
                time.sleep(0.5)
            except Exception as e:
                print(f"Error accessing clipboard: {e}")
                time.sleep(1)

    def add_bookmark(self, text):
        if text not in self.bookmarks:
            self.bookmarks.insert(0, text)
            self.save_data()
            self.update_menu()

    def remove_bookmark(self, text):
        if text in self.bookmarks:
            self.bookmarks.remove(text)
            self.save_data()
            self.update_menu()
    
    def is_bookmarked(self, text):
        return text in self.bookmarks

    def update_menu(self):
        self.menu.clear()
        self.menu.add(rumps.MenuItem("* Bookmarks", None))
        if not self.bookmarks:
            self.menu.add(rumps.MenuItem("  (No bookmarks)", None))
        else:
            for text in self.bookmarks:
                title = text[:60].replace("\n", " ") + ("..." if len(text) > 60 else "")
                item = rumps.MenuItem("* " + title, callback=self.copy_item)
                item.value = text
                item.add(rumps.MenuItem("Remove Bookmark", callback=lambda sender, t=text: self.remove_bookmark(t)))
                self.menu.add(item)
        self.menu.add(None)
        self.menu.add(rumps.MenuItem("Clipboard History", None))
        if not self.history:
            self.menu.add(rumps.MenuItem("  No items yet", None))
        else:
            for text in self.history:
                title = text[:60].replace("\n", " ") + ("..." if len(text) > 60 else "")
                item = rumps.MenuItem(title, callback=self.copy_item)
                item.value = text
                if self.is_bookmarked(text):
                    item.add(rumps.MenuItem("Remove Bookmark", callback=lambda sender, t=text: self.remove_bookmark(t)))
                else:
                    item.add(rumps.MenuItem("Add Bookmark", callback=lambda sender, t=text: self.add_bookmark(t)))
                self.menu.add(item)
        self.menu.add(None)
        self.menu.add(rumps.MenuItem("Clear History", callback=self.clear_history))
        self.menu.add(rumps.MenuItem("Quit", callback=self.quit_app))

    def copy_item(self, sender):
        pyperclip.copy(sender.value)
        rumps.notification("Clipboard Manager", "Copied to Clipboard", sender.value[:60])
        if sender.value in self.history:
            self.history.remove(sender.value)
            self.history.insert(0, sender.value)
            self.save_data()
            self.update_menu()

    def clear_history(self, sender):
        self.history = []
        self.save_data()
        self.update_menu()

    def quit_app(self, sender):
        rumps.quit_application()

if __name__ == "__main__":
    app = ClipboardApp()
    app.run()