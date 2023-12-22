import rumps
import threading
from tkinter import Tk, Button, Label, Entry, StringVar, messagebox
import requests

class AnkiDataEntryForm:
    def __init__(self):
        self.root = Tk()
        self.root.title("Anki Data Entry Form")

        # Variables to store user input
        self.front_var = StringVar()
        self.back_var = StringVar()
        self.deck_var = StringVar()
        self.tag_var = StringVar()
        self.audio_url_var = StringVar()
        self.video_url_var = StringVar()
        self.picture_url_var = StringVar()

        # Entry for Front (mandatory)
        Label(self.root, text="Front (mandatory):").pack()
        Entry(self.root, textvariable=self.front_var).pack()

        # Entry for Back (mandatory)
        Label(self.root, text="Back (mandatory):").pack()
        Entry(self.root, textvariable=self.back_var).pack()

        # Entry for Deck
        Label(self.root, text="Deck:").pack()
        Entry(self.root, textvariable=self.deck_var).pack()

        # Entry for Tags
        Label(self.root, text="Tags (comma-separated):").pack()
        Entry(self.root, textvariable=self.tag_var).pack()

        # Entry for Audio URL
        Label(self.root, text="Audio URL:").pack()
        Entry(self.root, textvariable=self.audio_url_var).pack()

        # Entry for Video URL
        Label(self.root, text="Video URL:").pack()
        Entry(self.root, textvariable=self.video_url_var).pack()

        # Entry for Picture URL
        Label(self.root, text="Picture URL:").pack()
        Entry(self.root, textvariable=self.picture_url_var).pack()

        # Button to add note
        Button(self.root, text="Add Note", command=self.add_note).pack()

    def add_note(self):
        # Get user input
        front = self.front_var.get()
        back = self.back_var.get()
        deck = self.deck_var.get()
        tags = [tag.strip() for tag in self.tag_var.get().split(",")]
        audio_url = self.audio_url_var.get()
        video_url = self.video_url_var.get()
        picture_url = self.picture_url_var.get()

        # Prepare note data
        note_data = {
            "note" : {
                "deckName": deck if deck else "Default",
                "modelName": "Basic",
                "fields": {"Front": front, "Back": back},
                "options": {"allowDuplicate": False, "duplicateScope": "deck", "duplicateScopeOptions": {"deckName": "Default", "checkChildren": False, "checkAllModels": False}},
                "tags": tags,
                "audio": [{"url": audio_url, "filename": "audio.mp3", "skipHash": "", "fields": ["Front"]}] if audio_url else [],
                "video": [{"url": video_url, "filename": "video.mp4", "skipHash": "", "fields": ["Back"]}] if video_url else [],
                "picture": [{"url": picture_url, "filename": "image.jpg", "skipHash": "", "fields": ["Back"]}] if picture_url else [],
            }
        }

        # Make API request to add note
        response = self.make_api_request("addNote", **note_data)

        # Print the payload for debugging
        print("API Response Payload:", response)

        # Show result
        if "error" in response and response["error"] is not None and isinstance(response["error"], int) and response["error"] != 0:
            messagebox.showerror("Error", f"Failed to add note. Error: {response['error']}")
        else:
            messagebox.showinfo("Success", "Note added successfully!")

        # Close the form after adding a note
        self.root.destroy()

    def make_api_request(self, action, **params):
        # AnkiConnect URL
        anki_connect_url = "http://localhost:8765"

        # Payload for the POST request
        payload = {"action": action, "version": 6, "params": params}

        # Print the payload for debugging
        print("API Request Payload:", payload)

        try:
            # Make the POST request to AnkiConnect
            response = requests.post(anki_connect_url, json=payload)
            response.raise_for_status()

            # Parse and return the JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return {"error": str(e)}

class AnkiMenuBarApp(rumps.App):
    def __init__(self):
        super(AnkiMenuBarApp, self).__init__("Anki")
        self.menu = ["Add Flashcard", "Quit"]

    @rumps.clicked("Add Flashcard")
    def add_flashcard(self, _):
        # Open the AnkiDataEntryForm when 'Add Flashcard' is clicked
        anki_data_entry_form = AnkiDataEntryForm()

        # Run the Tkinter app in a separate thread
        threading.Thread(target=anki_data_entry_form.root.mainloop).start()

    @rumps.clicked("Quit")
    def quit(self, _):
        rumps.quit_application()

if __name__ == "__main__":
    app = AnkiMenuBarApp()
    app.run()