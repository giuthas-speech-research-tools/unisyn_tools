import re
import sys
import time

def main(lexicon):
    input_lexicon = open(lexicon, "r")

    output_CV_lexicon = open(lexicon + "_CV.csv", "w")
    output_CV_html_ready = open(lexicon + "_CV", "w")

    output_monosyllable_lexicon = open(lexicon + "_monosyllable.csv", "w")
    output_monosyllable_html_ready = open(lexicon + "_monosyllable", "w")

    output_disyllable_lexicon = open(lexicon + "_disyllable.csv", "w")
    output_disyllable_html_ready = open(lexicon + "_disyllable", "w")

    CV_lexicon = []
    monosyllable_lexicon = []
    disyllable_lexicon = []

    # TODO: It looks a bit like unisyn maybe using \I instead of I\ and other such constructions
    # There are alsa a good number of @`r sequences that should be checked.
    vowels = "(i|y|1|}|M|u|I|Y|I\\|U\\|U|e|2|@\\|8|7|o|e_o|2_o|@|@`|o_o|E|9|3|3\\|V|O|{|6|a|&|a_\"|A|Q)"
    C = "[^" + vowels +"]"
    V = "[" + vowels +"]"
    V_re = re.compile(vowels)

    # These patterns are incomplete. 
    CV_pattern = re.compile("^" + C + V + "$")
    monosyllable_pattern = re.compile("^" + C + '?' + V + C + '?' + "$")
    disyllable_pattern = re.compile("^" + C + '?' + V + C + V + C + '?' + "$")

    for line in input_lexicon:
        # This splits the line to three fields:
        # 0 word:[ling info]:[ling info]:
        # 1 sampa representation
        # 2 :derivation:lexical frequency
        fields = line.strip().split()

        # We are only looking for 1 and 2 syllable words.
        # " marks a stressed syllable
        # $ marks an unstressed syllable
        if len(fields[1].split("[$\"]")) > 2:
            continue

        # If we want to choose only words with stressed initial syllable.
        # elif fields[1][0] != "\"":
        #     continue
        # If we want to choose only stressed monosyllable words.
        # elif len(fields[1][1:].split("\"")) > 1:
        #     continue

        # token = "".join(fields[1][1:].split("'"))
        # token = "".join(token.split("\\"))

        # remove syllable boundary markers
        token = "".join(fields[1][1:].split("\""))
        token = "".join(token.split("$"))
        # I don't think that this is a syllable boundary marker but seems to have been previously gotten rid off.
        token = "".join(token.split("\\"))

        if not (CV_pattern.match(token) or monosyllable_pattern.match(token) or disyllable_pattern.match(token)):
            continue

        # make a list with just the ortographical word as a field
        entry = [fields[0][0:-1].split(":")[0]]
        # add the sampa representation
        entry.append(fields[1])
        
        # new_fields.append(str(len(fields[1].split("$"))))
        
        # add the lexical frequency
        entry.append(fields[2][1:].split(":")[1])

        # split into individual sounds 
        # TODO: turn this into a function that knows sampa and eats words of any length        
        if CV_pattern.match(token):
            entry.append(token[:-2])
            entry.append(token[-2:-1])
            entry.append(token[-1:])
            CV_lexicon.append(entry)

        if monosyllable_pattern.match(token):
            entry.append(token[:-2])
            entry.append(token[-2:-1])
            entry.append(token[-1:])
            monosyllable_lexicon.append(entry)

        if disyllable_pattern.match(token):
            sounds = V_re.split(token)
            entry.extend(sounds)
            disyllable_lexicon.append(entry)

    CV_lexicon = sorted(CV_lexicon, key=lambda entry: entry[1])
    monosyllable_lexicon = sorted(monosyllable_lexicon, key=lambda entry: entry[1])
    disyllable_lexicon = sorted(disyllable_lexicon, key=lambda entry: entry[1])


    for entry in CV_lexicon:
        line = ";".join(entry) + "\n"
        output_CV_lexicon.write(line)

        html_ready = ":".join(entry[0:3]) + ": " + \
            entry[3] + " :" + ":".join(entry[4:6]) + "\n"
        output_CV_html_ready.write(html_ready)

    print("Processed " + str(len(CV_lexicon)) + " CV entries.")

    for entry in monosyllable_lexicon:
        line = ";".join(entry) + "\n"
        output_monosyllable_lexicon.write(line)

        html_ready = ":".join(entry[0:3]) + ": " + \
            entry[3] + " :" + ":".join(entry[4:6]) + "\n"
        output_monosyllable_html_ready.write(html_ready)

    print("Processed " + str(len(monosyllable_lexicon)) + " monosyllable entries.")

    for entry in disyllable_lexicon:
        line = ";".join(entry) + "\n"
        output_disyllable_lexicon.write(line)

        html_ready = ":".join(entry[0:3]) + ": " + \
            entry[3] + " :" + ":".join(entry[4:6]) + "\n"
        output_disyllable_html_ready.write(html_ready)

    print("Processed " + str(len(disyllable_lexicon)) + " disyllable entries.")


if (__name__ == '__main__'):
    t = time.time()
    main(sys.argv[1])
    elapsed_time = time.time() - t
    print('Elapsed time ' + str(elapsed_time))
