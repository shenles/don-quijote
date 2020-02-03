# Estimating the comprehensibility of Don Quijote
If an English-only speaker without formal knowledge of Spanish tried to read <i>El ingenioso hidalgo don Quijote de la Mancha</i>, what percentage of the vocabulary would they have a chance of understanding?

I accounted for two factors:  first, the percentage of vocabulary in the chapters that was composed of mainstream Spanish words recognizable by most English speakers; and second, the percentage of vocabulary in the chapters that was composed of cognates, or words that mean the same thing and are spelled similarly in English and Spanish.  Adding the two percentages gave me the overall percentage of vocab that was likely recognizable by an English-only speaker.

## Data Sources
1.  Plain text Don Quijote e-book in Spanish, available from Project Gutenberg at http://www.gutenberg.org/cache/epub/2000/pg2000.txt
2.  Online Plain Text English Dictionary (OPTED) at http://www.mso.anu.edu.au/~ralph/OPTED/

## Run Instructions
This is an older project written in Python 2, which is no longer supported. Running it is not recommended.

## Results
After a considerable amount of cleanup - isolating a particular chapter, removing inconsistencies in case, punctuation, accented characters, duplicate words, etc. - comparisons were made between the imported OPTED entries and the vocabulary of that chapter. Instances of popularly understood words were counted, as were instances of cognates. Comparing these counts to the total vocabulary count gave the percentage that would likely be comprehensible. This process was then performed for each chapter. Percentage comprehensibility varied between chapters, but was usually between 4-6 percent.

