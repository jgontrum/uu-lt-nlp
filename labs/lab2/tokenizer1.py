import re, sys

# Final regex:
# (?P<sent>(?<=[.!?])[«»‘“`´'"]|[.!?](?=\s|$))(?!\s*[a-z])|(?P<tok>(?:Nov|Dr|Ltd|Corp|Mr|Mrs|Co|Mass)\.|n't|'d|'s|'ll|[-'`´‘]{2,}|(?:\d+[.,]\d+)|(?:\w+\.){2,}|[A-Z]\.|[«»‘“`´'",;:.!?%\$&]|(?:\w(?!'t)(?:-(?!-))?)+)

# DEFINITIONS
#
#
# 'Mass' is not really an abbreviation, but meh.
abbreviation = "Nov Dr Ltd Corp Mr Mrs Co Mass".split()
suffixes = "n't 'm 're 've 'd 's 'll".split()
sentence_delimiter = ".!?"
quotes = "«»‘“`´'\""

# TOKENIZER
#
#

tokenizer_parts = []

# Highest priority: hard-coded abbreviation
tokenizer_parts.append(r"(?:{})\.".format("|".join(abbreviation)))

# "stem" endings like n't or 'd or 's
tokenizer_parts.append("|".join(suffixes))

# Multi symbol groups like --
tokenizer_parts.append(r"[-'`´‘]{2,}")

# Numbers with a separating point 12.32
tokenizer_parts.append(r"(?:\d+[.,]\d+)")
    
# Abbreviation like Ph.D. or V.I.P.
tokenizer_parts.append(r"(?:\w+\.){2,}")

# Capital single letter abbreviation like J.
tokenizer_parts.append(r"[A-Z]\.")

# Single symbols
tokenizer_parts.append(rf"[{quotes},;:.!?%\$&]")

# Basic token that may include a *single* dash.
tokenizer_parts.append(r"(?:\w(?!'t)(?:-(?!-))?)+")

# SENTENCE BOUNDARY DETECTION
#
#

sentence_parts = []

# Special case: Segment after sentence followed by quote character: token." New
sentence_parts.append(rf"(?<=[{sentence_delimiter}])[{quotes}]")

# Simple sentence segmentation: Use common characters that
# mark the end of a sentence and are followed by a whitespace.
sentence_parts.append(rf"[{sentence_delimiter}](?=\s|$)")

# Define constrains that prevents segmentations in certain cases.
# They are encapsuled in a negative lookahead.
sent_constraints = []

# Do not seperate if the next word starts with a small letter.
sent_constraints.append(r"\s*[a-z]")

# FINAL REGEX
#
#
# Use group names to combine the regular expressions for tokens
# and for sentences. Since we want to treat sentences differenty,
# we can separate the matches in this way.
regex = "(?P<sent>{sent}){sent_constraints}|(?P<tok>{tok})".format(
  sent="|".join(sentence_parts),
  sent_constraints="(?!{})".format("|".join(sent_constraints)),
  tok="|".join(tokenizer_parts)
) 

# Debug: Print used regex to stderr
print(regex, file=sys.stderr)

last_token = None
for line in sys.stdin:
    for match in re.finditer(regex, line.strip()):
      # See if the match originated from the 'sentence' regex
      # or from the 'tokenizer' regex.
      result = match.groupdict()

      if result.get("tok"):
        print(result["tok"])
        last_token = result["tok"]
      elif result.get("sent"):
        print(result["sent"])
        print()
        last_token = result["sent"]

# Add a final period to the end, if that has not already happened.
if last_token not in sentence_delimiter:
  print(".\n")


"".join([
  r"(?P<sent>(?<=[.!?])[«»‘“`´'\"]|[.!?](?=\s|$))(?!\s*[a-z])|",
  r"(?P<tok>",
  r"(?:Nov|Dr|Ltd|Corp|Mr|Mrs|Co|Mass)\.|n't|'d|'s|'ll|[-'`´‘]{2,}",
  r"|(?:\d+[.,]\d+)|(?:\w+\.){2,}|[A-Z]\.|[«»‘“`´'\",;:.!?%\$&]",
  r"|(?:\w(?!'t)(?:-(?!-))?)+)"
])
