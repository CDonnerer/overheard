# cm-overheard

Extract comments from arxiv source files.

## Installation

```
git clone {this}
cd {this}
pip install .
```

## Usage

There are two entrypoints available.

```
overheard fetch --data path/to/data
```

This will get all of today's submissions and extract their source files.

```
overheard comments --data path/to/data
```

This will extract the comments out of the `tex` source files.
