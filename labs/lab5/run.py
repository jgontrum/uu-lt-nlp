from subprocess import run, PIPE, DEVNULL

import progressbar
from scipy.optimize import brute

from score import scoreTokens


class HunPOS():
    TRAIN = "hunpos-train"
    TAG = "hunpos-tag"

    def __init__(self, out_dir="./"):
        self.out_dir = out_dir

    def _train(self, corpus, t=2, e=2, f=10, s=10):
        model_name = f"{self.out_dir}tagger_t={t}_e={e}_f={f}_s={s}"

        process = run([self.TRAIN, model_name,
                       "-t", str(t), "-e", str(e), "-f", str(f), "-s", str(s)],
                      input=corpus,
                      stderr=DEVNULL)

        return model_name if process.returncode == 0 else None

    def _tag(self, model, test_set):
        process = run([self.TAG, model],
                      input=test_set,
                      stderr=DEVNULL,
                      stdout=PIPE)

        # Delete model to save space
        # run(["rm", "-f", model])

        return [l.strip("\n\t") for l in process.stdout.decode().split("\n") if
                l] \
            if process.returncode == 0 else None

    @staticmethod
    def _score(gold_set, test_set):
        assert len(gold_set) == len(test_set)

        tokcount, errcount, tpcount, fpcount, fncount = \
            scoreTokens(1, zip(gold_set, test_set))

        return {
            "tokcount": tokcount,
            "errcount": errcount,
            "tpcount": tpcount,
            "fpcount": fpcount,
            "fncount": fncount
        }

    def accuracy_pipeline(self, train, test, gold, t=2, e=2, f=10, s=10):
        model = self._train(train, t=t, e=e, f=f, s=s)
        tagged = self._tag(model, test)
        scores = self._score(gold, tagged)

        return (scores['tokcount'] - scores['errcount']) / scores['tokcount']


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", help="Train corpus",
                        type=str, required=True)

    parser.add_argument("--test", help="Test corpus",
                        type=str, required=True)

    parser.add_argument("--gold", help="Gold corpus",
                        type=str, required=True)

    parser.add_argument("--hunpostrain", help="hunpos-train binart",
                        type=str, required=False, default="hunpos-train")

    parser.add_argument("--hunpostag", help="hunpos-tag binart",
                        type=str, required=False, default="hunpos-tag")


    parser.add_argument("--emin", help="e min value",
                        type=str, required=True, default="hunpos-tag")


    args = parser.parse_args()
    # Files and binaries
    train_file = args.train
    test_file = args.test
    gold_file = args.gold

    hun_pos_train_bin = args.hunpostrain
    hun_pos_tag_bin = args.hunpostag

    # Parameters:
    # See: https://code.google.com/archive/p/hunpos/wikis/UserManualI.wiki
    t_min = 4
    t_max = 4

    e_min = 3
    e_max = 3

    f_min = 14
    f_max = 14
    f_step = 1

    s_min = 6
    s_max = 6
    s_step = 1

    # Set up wrapper and read in files...
    hun = HunPOS()
    hun.TRAIN = hun_pos_train_bin
    hun.TAG = hun_pos_tag_bin

    train = open(train_file, 'rb').read()
    test = open(test_file, 'rb').read()
    gold = [l.strip("\n\t") for l in open(gold_file).readlines() if
            l and l != "\n"]

    iterations = (t_max + 1 - t_min) * (e_max + 1 - e_min) \
                 * (f_max + 1 - f_min) * (s_max + 1 - s_min)

    print("Performing grid search to find the best parameters...")

    with progressbar.ProgressBar(max_value=iterations) as bar:
        counter = 0

        # Define minimization function
        def fun(params):
            global counter
            bar.update(counter)
            counter += 1
            t, e, f, s = params
            return 1 - hun.accuracy_pipeline(train, test, gold,
                                             int(t), int(e), int(f), int(s))

        ranges = (
            slice(t_min, t_max + 1, 1),
            slice(e_min, e_max + 1, 1),
            slice(f_min, f_max + 1, f_step),
            slice(s_min, s_max + 1, s_step)
        )

        # Perform brute force search
        grid_search = brute(fun, ranges, full_output=True, finish=None)

    t_opt, e_opt, f_opt, s_opt = grid_search[0]

    print(f"Best Accuracy: {1 - grid_search[1]}")
    print(f"Optimal parameters: t={t_opt}, e={e_opt}, f={f_opt}, s={s_opt}")
