# TODO when updating pypi

- increase version number in setup.cfg
- manually copy updates files from master
- update README.md if any changes
- update src/binary_trie/trie.py if any changes
- update src/binary_trie/helpers.py if any changes
- add new .py files in src/binary_trie if any
- add new functions in imports in src/binary_trie/__init__.py

```
python3 -m build
python3 -m twine upload dist/*
rm -rf dist/
```

- push branch to repo
