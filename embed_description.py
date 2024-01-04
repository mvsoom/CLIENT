import numpy as np
import torch
from sentence_transformers import SentenceTransformer
import argparse


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL = (
    "all-MiniLM-L6-v2"
)  # Has a maximum sequence length of 256 tokens ~ 1000 chars ~ 200 words


def process_description(description):
    # Split the timestamp (first word) from the description (following words)
    timestamp, description = description.split(" ", 1)
    timestamp = float(timestamp)
    return timestamp, description


def unzip(l):
    return zip(*l)


def main(args):
    model = SentenceTransformer(MODEL)
    assert model.max_seq_length >= 128

    if args.verbose:
        print("Device:", DEVICE)
        print("Model:", MODEL, f"(max_seq_length={model.max_seq_length})")

    with open(args.description_file, "r") as f:
        text = f.read()

    timestamps, descriptions = unzip(
        [process_description(line) for line in text.splitlines()]
    )

    embeddings = model.encode(descriptions, convert_to_numpy=True, device=DEVICE)

    # Save the timestamps and embeddings
    output = args.description_file + ".npz"
    np.savez(output, timestamp=timestamps, embedding=embeddings)

    if args.verbose:
        print(f"Written {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Embed the descriptions in a timestamped .description file"
    )
    parser.add_argument("description_file", help="Path to the description file")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")

    args = parser.parse_args()

    exit(main(args))