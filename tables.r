
words = read.csv("gam_mono_and_di.csv", sep="\t", quote="")
names(words)


xtabs(~syllables+C1, data=words)
xtabs(~syllables+Cf, data=words)
xtabs(~syllables+C2, data=words, syllables == 2)
sum(xtabs(~syllables+C1, data=words))
