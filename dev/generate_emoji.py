#!/usr/bin/python3
import json
import re

with open("emojilib/dist/emoji-en-US.json") as f:
  meanings = json.load(f)
with open("unicode-emoji-json/data-by-emoji.json") as f:
  unicode_datas = json.load(f)
with open("unicode-emoji-json/data-emoji-components.json") as f:
  components = json.load(f)

light_skin_tone = components["light_skin_tone"]
medium_light_skin_tone = components["medium_light_skin_tone"]
medium_skin_tone = components["medium_skin_tone"]
medium_dark_skin_tone = components["medium_dark_skin_tone"]
dark_skin_tone = components["dark_skin_tone"]

replaceables = {
  "-1": "minus_one",
  "+1": "plus_one",
  "-": "_",
  " ": "_",
  "å": "a",
  "é": "e",
  "ç": "c",
  "é": "e",
  "keycap_1": "one",
  "keycap_2": "two",
  "keycap_3": "three",
  "keycap_4": "four",
  "keycap_5": "five",
  "keycap_6": "six",
  "keycap_7": "seven",
  "keycap_8": "eight",
  "keycap_9": "nine",
  "keycap_10": "ten",
}
valid = re.compile(r"^[a-z_]+$")

def get_tones(emoji):
  if unicode_datas[emoji]["skin_tone_support"]:
    return [
      emoji,
      emoji + light_skin_tone,
      emoji + medium_light_skin_tone,
      emoji + medium_skin_tone,
      emoji + medium_dark_skin_tone,
      emoji + dark_skin_tone]
  return [emoji]

with open("emoji.dict.yaml", "w") as f:
  f.write("""---
name: emoji
version: "20211114"
...
""")
  for emoji, meanings in meanings.items():
    # tones = get_tones(emoji)
    for meaning in meanings:
      meaning = meaning.lower()
      for fromch, toch in replaceables.items():
        meaning = meaning.replace(fromch, toch)
      if not valid.match(meaning):
        print(f"\"{meaning}\" is not a valid identifier, skipping")
        continue
      # for tone in tones:
      #   f.write(f"{tone}\t{meaning}\n")
      f.write(f"{emoji}|{meaning}\t{meaning.replace('_', '')}\n")
