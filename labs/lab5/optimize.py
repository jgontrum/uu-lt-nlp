from subprocess import Popen, PIPE, STDOUT

corpus = open("ewt-train-wt.txt", 'rt').read()

def execute(cmd):
    process = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    return process.communicate(input=corpus)

def train(t, e, f, s, corpus="ewt-train-wt.txt"):
    model = "model_t={}_e={}_f={}_s={}".format(t, e, f, s)
    execute(["hunpos-train", "model",
        "t", str(t), "e", str(e), "f", str(f), "s", str(s)])
    #execute("hunpos-train {model} t {t} e {e} f {f} s {s} < {corpus}".format(**locals()))


train(2, 2, 15, 15)
