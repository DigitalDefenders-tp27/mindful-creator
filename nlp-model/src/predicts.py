"""CLI wrapper to call inference.py without relative imports."""
import sys
import os
import argparse

# Ensure project root is on PYTHONPATH
top = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if top not in sys.path:
    sys.path.insert(0, top)

from inference import predict_texts


def main():
    parser = argparse.ArgumentParser(description="Predict via inference module.")
    parser.add_argument('texts', nargs='+', help='Texts to analyze')
    args = parser.parse_args()
    results = predict_texts(args.texts)
    for r in results:
        print(r)


if __name__ == '__main__':
    main()
