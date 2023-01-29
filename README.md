# FAVORITE-Unpacker

An update for [fvp-tools](https://github.com/vn-tools/fvp-tools)'s script (de)compiler. Tested on IroSekai only for now.

Complaints should be disregarded as many translation groups nowadays are performing proper translations, with proper teams that do engine work to ensure quality of a given novel. This is an update for those who are impatient (me) when it comes to release/announcement dates for certain translations and the quality will only depend on the work given to translation. Passing a script into a machine translation will obviously not net the best results but many MTL readers (namely LN/WN readers) live with these words:

[*Using machine translation cultivates a superior form of reading where you constantly have to use your imagination while thinking about multiple possibilites of meaning and developing a high contextual awareness, questioning every word and seeing every sentence as multiple possible sentences, composing your own story simultaneously to fill in the gaps and calculating uncertainties while contemplating the nature of ambiguity. Readers of Japanese just passively access memorised and thus already stagnant data, while MTL readers actively engage with the text on a much more fundamental level, being intellectually more in tune with the writer's intention and the truth of the text.*](https://www.reddit.com/r/visualnovels/comments/ka23le/reading_machine_translations_is_highly/)

Some degree of Japanese is suggested in order to identify discrepencies in translation. 

There are two main files:
## ScriptConversion.py
You run this file to convert a text-file line-by-line into deepL which spits out a translation. Originally this used deep_translator's GoogleTranslator, however many lines often return 'None' objects (e.g line "..."). Code added to circumvent this, but is not the main issue at the moment.
Running this program does not use deepL's api key so connection will begin throttling after about 1000 lines. Use a VPN to bypass limit for another ~1000 words before throttling. Obviously very inefficient.

### Pros:
- Actually works
- Works with "most" files (UTF-8 encoded, no "\xe9" characters please)
- Can be interrupted with Ctrl+C to flush buffer to file
- Current state of the translation is updated per translation in the format:
[CurrentLine / TotalLines] OriginalText -> TranslatedText

### Cons:
- Slow (Line-by-line works for my use-case, Will not bother improving unless a PR is posted that also circumvents throttling issue)
- Unreliable (Throttling) (Can implement some os functionality with Windscribe that toggles VPN once a line fails maybe soon)
- Lack of functionality (Names like "Shinku" is more often than not translated to "crimson" and needs to be modified manually)
On another note, It is possible to archive all character names and replace all occurences of that name with the correct, translated version prior to translating the rest of the text, but i'm not bothered with it.

### How to use it:
Just make sure you run this program with a "strings.txt" file in the relative location of where the program is ran (Obviously can modify code but not really a priority)

## HCB.py
This updates fvp-tools to support IroSekai, namely with opcodes that have an empty correlation - from the first ~2000 lines of gameplay, no issues have been found so far.

### How to use it:
Read [fvp-tools](https://github.com/vn-tools/fvp-tools) a more detailed explanation as the commands remain relatively the same.

### Issues
At times the length of a line can be too long. There is a limit of 255 characters for a single line, and if such an error rises the (index + 1) number denotes the line with the given string being printed to console. Modification must then be done manually to circumvent the issue.
Only certain types of characters can be read due to encoding. A UnicodeEncodeError exception will be raised if a certain character can't be read, and often these encoding issues will only arise due to translations. The line "Bon Appétit" will for example throw an error due to the accented e character (\xe9). The error message should print out the index of the character where the error is located at, so using your favourite IDE, you can modify that manually.
