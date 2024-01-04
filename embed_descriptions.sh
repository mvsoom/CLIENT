#!/bin/bash
export FIFTYONE_DATASET_ZOO_DIR="$(pwd)/dataset-zoo"

# Process all .description file
mapfile -t files < <(find $FIFTYONE_DATASET_ZOO_DIR -type f -name "*.description")
for file in "${files[@]}"; do
    python3 embed_description.py --verbose "$file"
done