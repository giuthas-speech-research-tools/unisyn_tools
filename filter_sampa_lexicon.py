import re
import sys
import time

def main(lexicon):
    input_lexicon = open(lexicon, "r")
    output_VC_lexicon = open(lexicon + "_VC.csv", "w")
    output_VC_html_ready = open(lexicon + "_VC", "w")
    output_CVC_lexicon = open(lexicon + "_CVC.csv", "w")
    output_CVC_html_ready = open(lexicon + "_CVC", "w")
    output_CCVC_lexicon = open(lexicon + "_CCVC.csv", "w")
    output_CCVC_html_ready = open(lexicon + "_CCVC", "w")
    output_CCCVC_lexicon = open(lexicon + "_CCCVC.csv", "w")
    output_CCCVC_html_ready = open(lexicon + "_CCCVC", "w")

    CCCVC_lexicon = []
    CCVC_lexicon = []
    CVC_lexicon = []
    VC_lexicon = []

    # aio}
    CCCVC_pattern = re.compile("[^aVeEiIoO}]{3}[aVeEiIoO}][ptk?]$")
    CCVC_pattern = re.compile("[^aVeEiIoO}]{2}[aVeEiIoO}][ptk?]$")
    CVC_pattern = re.compile("[^aVeEiIoO}][aVeEiIoO}][ptk?]$")
    VC_pattern = re.compile("^[aVeEiIoO}][ptk?]$")
    gen_pattern = re.compile("[^aVeEiIoO}]{1,3}[aVeEiIoO}][ptk?]$")


    for line in input_lexicon:
        fields = line.split()

        # We are only looking for 1 and 2 syllable words.
        if len(fields[1].split("$")) > 1:
            continue
    #    elif fields[1][0] != "\"":
    #        continue
        elif len(fields[1][1:].split("\"")) > 1:
            continue

        token = "".join(fields[1][1:].split("'"))
        token = "".join(token.split("\\"))
        if not (gen_pattern.match(token) or VC_pattern.match(token)):
            continue

        entry = fields[0][0:-1].split(":")
        entry.append(fields[1])
        # new_fields.append(str(len(fields[1].split("$"))))
        entry.extend(fields[2][1:].split(":"))
        
        if CCCVC_pattern.match(token):
            entry.append(token[:-2])
            entry.append(token[-2:-1])
            entry.append(token[-1:])
            CCCVC_lexicon.append(entry)
        elif CCVC_pattern.match(token):
            entry.append(token[:-2])
            entry.append(token[-2:-1])
            entry.append(token[-1:])
            CCVC_lexicon.append(entry)
        elif CVC_pattern.match(token):
            entry.append(token[:-2])
            entry.append(token[-2:-1])
            entry.append(token[-1:])
            CVC_lexicon.append(entry)
        else:
            entry.append(token)
            entry.append(token[0:1])
            entry.append(token[-1:])
            VC_lexicon.append(entry)

    CCCVC_lexicon = sorted(CCCVC_lexicon, key=lambda entry: entry[3])
    CCVC_lexicon = sorted(CCVC_lexicon, key=lambda entry: entry[3])
    CVC_lexicon = sorted(CVC_lexicon, key=lambda entry: entry[3])
    VC_lexicon = sorted(VC_lexicon, key=lambda entry: entry[3])

    for entry in CCCVC_lexicon:
        line = ";".join(entry) + "\n"
        output_CCCVC_lexicon.write(line)

        html_ready = ":".join(entry[0:3]) + ": " + \
            entry[3] + " :" + ":".join(entry[4:6]) + "\n"
        output_CCCVC_html_ready.write(html_ready)

    for entry in CCVC_lexicon:
        line = ";".join(entry) + "\n"
        output_CCVC_lexicon.write(line)

        html_ready = ":".join(entry[0:3]) + ": " + \
            entry[3] + " :" + ":".join(entry[4:6]) + "\n"
        output_CCVC_html_ready.write(html_ready)

    for entry in CVC_lexicon:
        line = ";".join(entry) + "\n"
        output_CVC_lexicon.write(line)

        html_ready = ":".join(entry[0:3]) + ": " + \
            entry[3] + " :" + ":".join(entry[4:6]) + "\n"
        output_CVC_html_ready.write(html_ready)

    for entry in VC_lexicon:
        line = ";".join(entry) + "\n"
        output_VC_lexicon.write(line)

        html_ready = ":".join(entry[0:3]) + ": " + \
            entry[3] + " :" + ":".join(entry[4:6]) + "\n"
        output_VC_html_ready.write(html_ready)


    print("Processed " + str(len(CCCVC_lexicon)) + " CCCVC entries, " + 
        str(len(CCVC_lexicon)) + " CCVC entries, " + 
        str(len(CVC_lexicon)) + " CVC entries and " + 
        str(len(VC_lexicon)) + " VC entries.")

if (__name__ == '__main__'):
    t = time.time()
    main(sys.argv[1])
    elapsed_time = time.time() - t
    print('Elapsed time ' + str(elapsed_time))
