import cfg_parser as cfg

g = cfg.read_grammar('grammar.txt')

sentences = [
   "He worked for the BBC for a decade.",
   "She spoke to CNN Style about the experience.",
   "Global warming has caused a change in the pattern of the rainy seasons.",
   "I also wonder whether the Davis Cup played a part.",
   "The scheme makes money through sponsorship and advertising."
]

for i, s in enumerate(sentences):
    print(i, cfg.parse_sentence(g, s))

