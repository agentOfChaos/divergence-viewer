# divergence-viewer
Provide a visual hash of the current timeline, useful for theoretical time travelers

# Abstract

Sometimes, when people around me behave differently from their usual, I jokingly ask
the date of the fall of Berlin' wall (1989, right?), to "check if I ended up in a
parallel universe/timeline".

So, I asked myself if I could make an automated tool to check for differences, just like
the divergence meter from the anime/visual novel Steins;gate.

This tool shows not an actual number, but a picture more similar to the "randomart" used
to validate ssh keys.

# Dependencies

(See requirements.txt)

    requests
    beautifulsoup4
    Pillow
    romkan
    colorama

# Usage

    ./diviewer.py

Note that it may take some time to re-download the stock history data, depending on the current date
and the "initial date" defined by the program.

## How it works

Basically, the program downloads a list of historical stock data in chronological order, and then generates a
series of hashes using each data sample.
The hashes are built chaining the value of sample X with the hash of sample X-1, thus creating a chain in which
every member depends on its predecessors in a non-linear way.
This resulting hash-chain is presented in a human-readable form.


### Why?

I chose to use stock data since they're objective, easy to look-up in an automated way,
and thoroughly recorded; on top of that, the stock prices are deeply influenced by
historical events and social turmoils (albeit in a chaotic, indirect way), thus allowing the
program to indirectly perceive "changes in history".

The hash-chain technique propagates the error with a cascade effect, so that a change in older records
will have a more visible effect than a change in recent records.


## Interpreting the output

(Note: the normal output is built using japanese katakana; a romanized version is available by running `./diviewer.py -r`)
(Note 2: the output may look garbled inside a console with a non-monospace font; to overcome this, you may
output a rendered image using `./diviewer.py -i image.png`)

    +-[ 2000-01-01 ]-+
    |ナビカトタゴエギ|
    |バ            シ|
    |ゾ  ゲガビゼゼキ|
    |ゾ  デ      ズレ|
    |()  ロ  カヨギト|
    |サ  ヌ  ()ブミド|
    |ノ  オブハド()ネ|
    |スマフスミカネマ|
    |    ゼアプペハド|
    +-[ 2018-11-14 ]-+

The graph is built as an outward clockwise spiral; each cell containing a syllable.  
Every single cell is a visual representation of an hash value.  
The "「"-shaped spaces were added to improve readability, plus they look kinda cool.  
The spiral originates from the innermost "()" (the first cell is located directly above it); 
the following "()" pairs separate the three classes of cells:

* the cells in the innermost spire represent hashes sampled with a 250-days period
* the cells following the second "()" encountered represent hashes sampled with a 25-days period
* the cells following the last "()" represent the hash taken a day apart from each other

A special algorithm is used to decide how to construct each class; samples belonging to the outermost classes
will be periodically compacted to save space.

The dates shown above and below the diagram indicate the time period spanned by the data samples shown in the figure.

# More help

    ./diviewer.py -h
