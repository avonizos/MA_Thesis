This project contains the source files, programs and results' tables for my Master thesis on the topic "Reconstruction of the Old Chinese phonology based on computational linguistic analysis of the Shijing rhymes"

------------------------------------------------------------------------------------------------------------------------------------------
STRUCTURE
------------------------------------------------------------------------------------------------------------------------------------------
1) folder _convert_:
- programs for obtaining the IPA transcriptions/romanisations for the characters in Shijing
- dialects: Fuzhou, Taiwanese Hokkien, Taiwanese Hakka, Cantonese

2) folder _to\_ipa_:
- programs for conversion from the romanisation systems to IPA
- dialects: Taiwanese Hokkien, Taiwanese Hakka, Cantonese

3) _find_rhymes.py_:
- search for rhymes in the different IPA versions
- looks for rhymes in the same stanza, +-5 lines from the current
- writes down the rhyming pair, the type of the rhyme (inexact, exact) and rhyming (paired, crossed, encircling)
- counts some relevant statistics

4) _disambiguate.py_:
- semi-automatic disambiguation of the words in the rhyming position
- user has to choose one of the pronunciations, comparing it with the Mandarin pronunciation and if possible with rhyming characters in Mandarin version of Shijing

5) _reconstruct.py_:
- semi-automatic reconstruction of an old pronunciation of the Chinese characters
- the program shows five aligned initials, finals of the syllables
- user has to decide how to reconstruct them