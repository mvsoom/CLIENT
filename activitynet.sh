#!/bin/bash
export FIFTYONE_DATASET_ZOO_DIR="$(pwd)/dataset-zoo"

# Function to process the video
process_sample() {
    OUTPUT="$1.description"

    # Skip if already processed earlier
    if [ -e "$OUTPUT" ]; then
        echo "$OUTPUT: already processed"
        return
    fi

    python3 describe_stream.py --timestamp "$1" > "$OUTPUT"
    exit_code=$?

    if [ $exit_code -ne 0 ]; then
        # Delete the descriptions file if the command was not successful
        echo "$OUTPUT: failed"
        rm "$OUTPUT"
    else
        echo "$OUTPUT: success"
    fi
}

# There are three splits: train, test, validation
BATCHSIZE_PER_SPLIT=100

while true; do
    # Batch download samples
    fiftyone zoo datasets load activitynet-200 \
        --kwargs max_samples=$BATCHSIZE_PER_SPLIT shuffle=True

    # Process all samples (.mp4) files
    mapfile -t samples < <(find . -type f -name "*.mp4")
    for sample in "${samples[@]}"; do
        process_sample "$sample" 2>&1 | tee -a $0.processed
        rm "$sample"
    done
done