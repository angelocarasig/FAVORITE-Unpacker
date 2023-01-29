from deep_translator import (GoogleTranslator)
import deepl
from time import sleep

def readToArray(input_file):

    result = []

    with open(input_file, "r", encoding='UTF-8') as f:
        line = f.readline()
        print(line)

        while line != '':
            result.append(line)
            line = f.readline()

    result = list(map(lambda x: x.strip(), result))

    for i in range(5):
        print(result[i])
    return result

def translateArray(input_array):


    with open('output.txt', 'w', encoding='UTF-8') as f:
        for index, word in enumerate(input_array):
            successfulTranslation = False            
            result = None
            while successfulTranslation == False:
                try:
                    result = deepl.translate(source_language="JA", target_language="EN", text=word)
                    successfulTranslation = True
                except:
                    print("Error translating...\nSleeping for 5 seconds...")
                    sleep(5)

            if (result == None):
                print(f"Wrote {word} instead of {result}...")
                f.write(word)
            else:
                print(f"[{index + 1} / {len(input_array)}] {word} -> {result}") 
                f.write(f"{result}\n")
            


def main():
    array = readToArray("strings.txt")
    translateArray(array)

if __name__=="__main__":
    main()
