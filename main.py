    import pyautogui
    import time
    import pyperclip  # To import content from clipboard
    import re
    import g4f
    from g4f.Provider import MetaAI   # ✅ Import provider properly


    def is_last_message_not_from_me(chat_text):
        """
        Returns True if the last WhatsApp message is NOT from 'ANUJ MATHUR'.
        """
        # Match only valid WhatsApp messages
        pattern = r"\[\d{1,2}:\d{2}\s*(?:am|pm)?,\s*\d{1,2}/\d{1,2}/\d{2,4}\]\s*([^:]+):"
        matches = re.findall(pattern, chat_text)

        if not matches:
            return False  # No valid messages found

        last_sender = matches[-1].strip().upper()
        return last_sender != "ANUJ MATHUR"


    def aiprocess(command):
        try:
            # Step 1: Click on the chrome icon
            pyautogui.click(1379, 1042)
            time.sleep(1)

            # Step 2: Drag the mouse to select text
            pyautogui.moveTo(928, 307)
            pyautogui.dragTo(1811, 905, duration=1.0, button="left")

            # Step 3: Copy the selected text to the clipboard
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(1)
            pyautogui.click(1339, 424)

            # Step 4: Retrieve the text from the clipboard
            chat_history = pyperclip.paste()
            print("[DEBUG] Copied chat history:\n", chat_history)

            # ✅ Check if last message is from someone else
            if not is_last_message_not_from_me(chat_history):
                print("[DEBUG] Last message is from YOU. No reply sent.")
                return "[INFO] Skipped: Last message is yours."

            # Step 5: Send to AI
            response = g4f.ChatCompletion.create(
                model="gpt-4o",
                provider=MetaAI,
                messages=[
                    {"role": "system", "content": "You are a person named Anuj who speaks hindi as well as english. You are from India and you are a coder. You analyze the chat history and respond naturally as Anuj. Output should be the next chat response as Anuj. Keep it short and clear!"},
                    {"role": "user", "content": chat_history}
                ],
                stream=False
            )

            # Ensure response is string
            reply = response if isinstance(response, str) else str(response)
            print("AI Reply:\n", reply)

            # Step 6: Paste into chatbox and press Enter
            pyperclip.copy(reply)  # Copy AI response
            pyautogui.click(1464, 943)  # Click on input box
            time.sleep(0.5)
            pyautogui.hotkey("ctrl", "v")  # Paste response
            time.sleep(0.3)
            # pyautogui.press("enter")  # Press Enter to send

            return reply
        
        except Exception as e:
            return f"[ERROR] {str(e)}"


    # Test run
    print(aiprocess("Test"))
