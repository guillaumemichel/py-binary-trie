# TODO when updating pypi

- increase version number in setup.cfg
- update README.md if any changes
- update src/binary_trie/trie.py if any changes
- update src/binary_trie/helpers.py if any changes

```
python3 -m build
python3 -m twine upload dist/*
rm -rf dist/
```

- update repo
