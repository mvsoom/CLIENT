# Transcribing the ActivityNet into descriptions

## Installation
I used Python 3.11.4, but other versions probably work fine too.

Download, setup venv, then
```bash
pip install -r requirements
```

## Usage
This repo transcripts video streams from the ActivityNet database into `.description` files.

The videos are downloaded in random batches using FiftyOne. Watch out, because running this script for too long ~~can~~will get you banned from YouTube.

The `camera-server` must run on the local net for this client to work, as it queries the server worker at http://localhost:40000.

You can start transcribing ActivityNet into descriptions with
```bash
cd [ROOT OF THIS REPO]
./activitynet.sh 2>&1 | tee activitynet.sh.log
```

## Statistics
Here is some pseudo code together with some outputs.
```bash
$ cd ./dataset-zoo

# Number of .description files (videos watched)
$ find . -type f -name "*.description" | wc -l
6603

# Number of descriptions (text lines)
$ find . -type f -name "*.description" -exec cat {} \; | wc -l
326815

# Number of words including timestamps
$ find . -type f -name "*.description" -exec cat {} \; | wc -w
25747879

# Number of words excluding timestamps (in the descriptions only)
= 25747879 - 326815 = 25421064 = 25M words = 34M tokens

# Cat a random description file
$ find . -type f -name "*.description" | shuf -n 1 | xargs cat

# Cat a random description file without timestamps
$ find . -type f -name "*.description" | shuf -n 1 | xargs cat | cut -d" " -f2-
```