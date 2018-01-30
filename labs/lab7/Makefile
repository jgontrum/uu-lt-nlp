

err:
	python lemmatizer.py < ewt-dev-wt.txt 2>&1 > /dev/null

lemmatize:
	python lemmatizer.py < ewt-dev-wt.txt > ewt-dev-out.txt 2>/dev/null

diff: lemmatize
	vimdiff ewt-dev-wtl.txt ewt-dev-out.txt

score: lemmatize
	python score.py lemma ewt-dev-wtl.txt ewt-dev-out.txt

analysis: lemmatize
	comm -2 -3 <\(sort ewt-dev-wtl.txt\) <\(sort ewt-dev-out.txt\) | uniq -cd | sort -nr
