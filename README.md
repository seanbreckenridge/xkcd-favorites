# [xkcd-favorites](https://seanbreckenridge.github.io/xkcd-favorites/)

A github pages website that lists my favorite [xkcd](https://xkcd.com)'s.

The MIT License applies to the code in this repository, I claim no ownership to the comics; [xkcd](https://xkcd.com/) is licensed under [CC BY-NC 2.5](https://creativecommons.org/licenses/by-nc/2.5/)

### Create your own!

If you wish to create your own favorites list, you can:

1. Fork this repository
2. `git clone ...` your repository to your computer.
3. Edit `favorites.yaml` to have your the corresponding IDs for your favorite xkcd's. The IDs are in the URL when viewing an xkcd.
4. `pip3 install -r requirements.txt`
5. `python3 generate.py`
6. `git push`

`generate.py` will use `data.json` as a cache, so any items previously downloaded won't have to be downloaded again.

For debugging whether or not something has already been downloaded, you can increase log verbosity by editing the `LOGLEVEL` envionment variable; e.g.:

`LOGLEVEL=DEBUG python3 generate.py`

More about log levels [here](https://docs.python.org/3.7/howto/logging.html#when-to-use-logging).
