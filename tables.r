
words = read.csv("stimulus_selection/gam_mono_and_disyllables.csv", sep="\t", quote="")
names(words)

# Check for duplicates and (near) homophones.
words[duplicated(words$word),]
words[duplicated(words$pronunciation_stripped),]

xtabs(~V1+V2+syllables, data=words)

xtabs(~V1+C2+syllables, data=words)

xtabs(~syllables+C1, data=words)
xtabs(~syllables+Cf, data=words)
xtabs(~syllables+C2, data=words)
sum(xtabs(~syllables+C1, data=words))

xtabs(~C1+C2, data=words, syllables == 2 & V1 == 'i')

# for culling some words from the i set
xtabs(~Cf, data=words, syllables == 2 & V1 == 'i')
xtabs(~C1, data=words, syllables == 2 & V1 == 'i')
xtabs(~C2, data=words, syllables == 2 & V1 == 'i')

sum(xtabs(~syllables+C1, data=words))
