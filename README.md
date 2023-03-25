# FAVORITE-Unpacker
Last Updated: 25/03/2023
----
An update for [fvp-tools](https://github.com/vn-tools/fvp-tools)'s script (de)compiler. Tested on IroSekai only for now.

Proper teams do proper translations nowadays, but some kamigames may never be translated. This is an update for those who are impatient (me) when it comes to release/announcement dates for certain translations. Passing a script into a machine translation will obviously not net the best results but many MTL readers (namely LN/WN readers) live by these words:

[_Using machine translation cultivates a superior form of reading where you constantly have to use your imagination while thinking about multiple possibilites of meaning and developing a high contextual awareness, questioning every word and seeing every sentence as multiple possible sentences, composing your own story simultaneously to fill in the gaps and calculating uncertainties while contemplating the nature of ambiguity. Readers of Japanese just passively access memorised and thus already stagnant data, while MTL readers actively engage with the text on a much more fundamental level, being intellectually more in tune with the writer's intention and the truth of the text._](https://www.reddit.com/r/visualnovels/comments/ka23le/reading_machine_translations_is_highly/)

Some degree of Japanese is suggested in order to identify and ignore discrepencies in translation to minimize confusion.

----

There are two main files:

## HCB.py
Uplifted version of [fvp-tools](https://github.com/vn-tools/fvp-tools). This updates fvp-tools to support IroSekai, namely with opcodes that have an empty correlation - from the first ~2000 lines of gameplay, no issues have been found so far. May work with other games, most likely with ones older than non-HD iroseka.

**How to use it**:
Read [fvp-tools](https://github.com/vn-tools/fvp-tools) for a more detailed explanation as the commands remain relatively the same.

## ScriptConversion.py
Run this file to open up a GUI that asks for an input text and an output file to save it to. Pass in the input_strings file generated from HCB.py.
Running this program does not use DeepL's api key (free or paid) so connection will begin throttling after about 1000 lines. Use a VPN to bypass limit for another ~1000 words before throttling. Obviously very inefficient.

----

### Pros:
- Actually works
- Works with "most" files (UTF-8 encoded, no "\xe9" characters please)
- Shows current line being translated

### Cons:
- Slow
- Unreliable (Throttling)
- Lack of functionality (Names like "Shinku" is more often than not translated to "crimson" and needs to be modified manually)

### Issues
- Limit of 255 characters per line
- Only certain lines can be read due to encoding ("Bon Appétit" throws error)
- Opcode unreadability for other non-iroseka programs

### To Do
- Add scroll when lines are overflown
- Dark mode
- Name whitelist (So Shinku != Crimson)
- Add VPN switching support
- Copy original .txt to a local folder
- Add different translation options
    - Extension: Add DeepL Free/Pro API key integration (maybe once Australia becomes a country that can use it T_T)
- Resolve issues

### Much Later To Dos
- Home screen
- Reverse engineer other developer script files (or find some online)
- Settings tab
- Multithreading

### Patch Notes

* 25/03/2023 - GUI Version