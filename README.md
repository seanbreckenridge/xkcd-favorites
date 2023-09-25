# [xkcd-favorites](https://sean.fish/xkcd/)

A GitHub pages website that lists my favorite [xkcd](https://xkcd.com)'s.

The MIT License applies to the code in this repository, I claim no ownership to the comics; [xkcd](https://xkcd.com/) is licensed under [CC BY-NC 2.5](https://creativecommons.org/licenses/by-nc/2.5/)

If you wish to create your own favorites list, you can:

1. Fork this repository
2. `git clone ...` your repository to your computer.
3. Edit `favorites.yaml` to have your the corresponding IDs for your favorite xkcd's. The IDs are in the URL when viewing an xkcd.
4. `pip3 install -r requirements.txt`
5. `python3 generate.py`

Then, either push the branch and use github pages, or host the `index.html`, `custom.css` and `index.js` on a website somewhere.

`generate.py` will use `data.json` as a cache, so any items previously downloaded won't have to be downloaded again.

For debugging whether or not something has already been downloaded, you can increase log verbosity by editing the `XKCD_LOGLEVEL` environment variable; e.g.:

`XKCD_LOGLEVEL=DEBUG python3 generate.py`

More about log levels [here](https://docs.python.org/3.7/howto/logging.html#when-to-use-logging).

I've also included a script [ssg](./ssg) which 'pre-renders' the page, removing the javascript from the page so there's no rendering client side. After I clone this to my server, I do: `./ssg && mv static.html index.html`.
