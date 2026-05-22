import os

YT_APIKEY = os.environ.get("YT_APIKEY", "AIzaSyA7kE8jee3x55TonmeiU-ZPdYLijju9Mho")
GEMINI_APIKEY = os.environ.get("GEMINI_APIKEY", "AIzaSyCuP_Z30Gy5Ow4T1W3V22bh7KF0o5dFy0U")

CHANNELS = [
    ("UCXUPKJO5MZQN11PqgIvyuvQ", "Andrej Karpathy"),
    ("UCSHZKyawb77ixDdsGog4iWA", "Lex Fridman"),
    ("UCZHmQk67mSJgfCCTn7xBfew", "Yannic Kilcher"),
    ("UCbfYPyITQ-7l4upoX8nvctg", "Two Minute Papers"),
    ("UCNJ1Ymd5yFuUPtn21xtRbbw", "AI Explained"),
]

MAX_VIDS_PERCHANNEL = 3