from .core_fuc import read_f


class Emoji:
    emojis: list = read_f("emoji.json")

    def replace_text_to_emoji(self, text):
        for emoji in self.emojis:
            emoji_text = f":{emoji.split(':')[1]}:"
            text.replace(emoji_text, emoji)
        return text
