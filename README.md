# divergence-viewer
Provide a visual hash of the current timeline, useful for theoretical time travellers

# Abstract

Sometimes, when people around me behave differently from their usual, I jokingly ask
the date of the fall of Berlin' wall (1989, right?), to "check if I ended up in a
parallel universe/timeline".

So, I asked mysef if I could make an automated tool to check for differences, just like
the divergence meter from the anime/visual novel Steins;gate.

This tool shows not an actual number, but a picture more similar to the "randomart" used
to validate ssh keys.

# Dependancies

    romkan
    pandas
    colorama

# Usage

    ./diviewer.py

Note that it may take some time to re-download the stock history cache (but it only
needs to do it once a day)

## How it works

Basically, it download historical financial data, computes hash values from them (in a
smart way), and then displays the result in a human-friendly way.

Just kidding, it hashes the data in a stupid way, and outputs the results in japanese.

### Why?

I chose to use stock data, since they're objective, easy to look-up in an automated way,
and thoroughly recorded; on top of that, the stock prices are deeply influenced by
major historical events (albeit in a chaotic, indirect way).  
More specifically, i use the yahoo finance api to query for the opening value of
the IBM stock, during a time period spanning from 1971 to today.

## Interpreting the output

(Note: the normal output is built using japanese katakana, this romanized version
is generated by running `./diviewer.py -r`)
(Note 2: either the pandas or yahoo developers changed something in the backend, 
thus making this older example no longer valid. After 2014-04-09, the program
was updated to take it into account.)

    +---[ 2016-07-23 ]---+
    |rogibosakoaakega    |
    |re                  |
    |()  yozumareyubimozo|
    |tu  mu            go|
    |bo  re  kehibisomoro|
    |ru  ri  ni      teso|
    |se  re  hi  timakore|
    |zu  pi  pa  ()ribepo|
    |ni  wa  biuutumeooku|
    |bo  iibuzitasoburude|
    |wayu()botufubizomuyo|
    +----[ 7dc28c60 ]----+

The graph is built as an outward clockwise spiral, by square cells made up of 2-letter syllabes.  
Each is a visual representation of an hash value (the first 4 bytes of today's hash are also
shown at the bottom, while the date itself is placed in the top part).  
The 「 shaped spaces are added to improve readability, plus they look kinda cool.  
The spiral origins in the innermost "()"; the following "()" pairs separate the
three classes of cells:

* the cells in the innermost spires represent each the hash of a 250-days period
* the cells between following the second "()" encountered represent the hash of a 25-days period
* the cells following the last "()" represent the hash of a single day

The hash of each single day is computed by also aggregating the hash of the previous one, so that
a minimal modification in any point of the sequence would results in huge differences in
the graph.

# More help

    ./diviewer.py -h
