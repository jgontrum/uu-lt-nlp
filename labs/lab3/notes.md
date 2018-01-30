# Lab3

# Bigrams
## 3.1
Number of types: 
`wc -l holmes-bigrams.txt`
= 111577

Number of tokens:
`awk -F'\t' '{ counter+=$3 } END { print counter }' holmes-bigrams.txt`
= 385372

## 3.2
Most frequent bigram:
`sort -k 3 -nr holmes-bigrams.txt | head -n 1`
(., <e>) occurs 13782 times (what a surprise!)

Most frequent bigram w/o bos/eos:
`egrep -v "<e>|<s>" holmes-bigrams.txt | sort -k 3 -nr | head -n 1`
(', and) occurs 4114 times.

## 3.3
Sherlock Holmes:
`egrep "^Sherlock.+Holmes" holmes-bigrams.txt`
= 195

Holmes Sherlock:
= 0

## 3.4
Bigrams that occur only once:
`egrep "\s1$" holmes-bigrams.txt | wc -l`
= 77701

## 3.5
Bigrams that do not occur at all.

1. Size of the vocabulary: 15397
`sort holmes-tokens.txt | uniq | wc -l`
2. Upper bound: pow(size, 2) = 237067609
3. Upper bound - number of types: 237067609 - 111577 = 236956032

# Maximum Likelihood Estimation

## 4.1
The probability of a bigram models the probablity of it occurence in the given corpus.

## 4.2
This is a uniform probability distribution over all bigrams in the corpus. Their probability is not maximized.

## 4.3  

|(Sherlock, Holmes)| = 195
|{(w1, w2) | w1, w2 ∈ VOCABULARY}| = 237067609

192/237067609 = 0.00000081

## 4.4

|(Holmes, Sherlock)| = 0
|{(w1, w2) | w1, w2 ∈ VOCABULARY}| = 237067609

0/237067609 = 0

# Probability estimates

## 5.1
## Marginal probability

Sum up all the joint probabilities where w1 occurs in the first position.
P(w1) = ∑{P(w1, w2) | w2 ∈ VOCABULARY}

## 5.2
## Conditional probability

P(w2|w1) = P(w1, w2) / P(w1)

