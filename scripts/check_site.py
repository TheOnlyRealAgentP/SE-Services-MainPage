#!/usr/bin/env python3
"""Check the built site for problems before publishing.

Usage:
    bundle exec jekyll build
    python3 scripts/check_site.py            # checks ./_site

Checks every page for:
  - internal links and images that don't resolve to a built file
  - href="#" placeholder links
  - <title> present, unique and <= 60 characters
  - meta description present, unique and <= 155 characters
  - exactly one <h1>
  - every JSON-LD block parses as JSON
  - every <img> has an alt attribute
  - double-escaped ampersands (&amp;amp;)
It also counts open TODOs, whether shown as markers or hidden as comments,
and fails if the word TODO shows up as ordinary page text.
Uses only the Python standard library. Exits with status 1 if anything fails.
"""
import json
import os
import re
import sys
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

SITE = sys.argv[1] if len(sys.argv) > 1 else "_site"
OWN_HOSTS = {"stewartengineeringservices.com", "www.stewartengineeringservices.com"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.imgs, self.jsonld = [], [], []
        self.title, self.desc, self.h1 = None, None, 0
        self.redirect = False
        self._in_title = self._in_ld = False
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        elif tag in ("link", "script", "source", "iframe"):
            # stylesheets, icons, canonical URLs, scripts, <picture> sources
            for v in (a.get("href"), a.get("src")):
                if v:
                    self.links.append(v)
            if a.get("srcset"):
                self.links += [p.strip().split(" ")[0] for p in a["srcset"].split(",")]
        if tag == "img":
            self.imgs.append(a)
            if a.get("src"):
                self.links.append(a["src"])
            if a.get("srcset"):
                self.links += [p.strip().split(" ")[0] for p in a["srcset"].split(",")]
        if tag == "title":
            self._in_title, self._buf = True, []
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        if tag == "meta" and a.get("http-equiv", "").lower() == "refresh":
            self.redirect = True
            target = a.get("content", "").split("url=", 1)[-1]
            self.links.append(target)
        if tag == "h1":
            self.h1 += 1
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld, self._buf = True, []

    def handle_endtag(self, tag):
        if tag == "title" and self._in_title:
            self.title, self._in_title = "".join(self._buf).strip(), False
        if tag == "script" and self._in_ld:
            self.jsonld.append("".join(self._buf))
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title or self._in_ld:
            self._buf.append(data)


def resolves(path):
    """Mirror GitHub Pages: /x serves x, x.html or x/index.html."""
    path = unquote(path).lstrip("/")
    full = os.path.join(SITE, path)
    if path == "" or path.endswith("/"):
        return os.path.isfile(os.path.join(full, "index.html"))
    return os.path.isfile(full) or os.path.isfile(full + ".html") or os.path.isfile(os.path.join(full, "index.html"))


def main():
    errors, titles, descs, todos = [], {}, {}, {}
    pages = []
    for root, _, files in os.walk(SITE):
        for f in files:
            if f.endswith(".html"):
                pages.append(os.path.join(root, f))
    pages.sort()

    for fp in pages:
        rel = "/" + os.path.relpath(fp, SITE)
        raw = open(fp, encoding="utf-8").read()
        p = Page()
        p.feed(raw)

        if 'href="#"' in raw:
            errors.append(f'{rel}: has href="#"')
        if "&amp;amp;" in raw:
            errors.append(f"{rel}: double-escaped ampersand (&amp;amp;)")

        for link in p.links:
            u = urlparse(link)
            if u.scheme in ("mailto", "tel", "data", "javascript"):
                continue
            if u.scheme in ("http", "https"):
                if u.netloc in OWN_HOSTS and not resolves(u.path or "/"):
                    errors.append(f"{rel}: broken absolute link {link}")
                continue
            if not u.path:          # pure #anchor or ?query on same page
                continue
            path = u.path if u.path.startswith("/") else os.path.join(os.path.dirname(rel), u.path)
            if not resolves(path):
                errors.append(f"{rel}: broken link {link}")

        for block in p.jsonld:
            try:
                json.loads(block)
            except ValueError as e:
                errors.append(f"{rel}: invalid JSON-LD ({e})")

        for img in p.imgs:
            if "alt" not in img:
                errors.append(f"{rel}: <img src={img.get('src')}> has no alt attribute")

        shown = len(re.findall(r'<mark class="todo">', raw))
        hidden = len(re.findall(r"<!-- TODO", raw))
        if shown or hidden:
            todos[rel] = (shown, hidden)
        # "TODO" must never appear as ordinary page text, only inside a
        # marker (show_todos: true) or an HTML comment (show_todos: false).
        body = raw.split("<body", 1)[-1]
        stray = re.sub(r"<!--.*?-->", "", body, flags=re.S)
        stray = re.sub(r'<mark class="todo">.*?</mark>', "", stray, flags=re.S)
        if "TODO" in stray:
            errors.append(f"{rel}: 'TODO' text outside a marker")

        if p.redirect:
            continue  # redirect stubs only need a working target

        if not p.title:
            errors.append(f"{rel}: missing <title>")
        else:
            t = unescape(p.title)
            if len(t) > 60:
                errors.append(f"{rel}: title is {len(t)} chars (max 60): {t}")
            titles.setdefault(t, []).append(rel)
        if not p.desc:
            errors.append(f"{rel}: missing meta description")
        else:
            d = unescape(p.desc)
            if len(d) > 155:
                errors.append(f"{rel}: description is {len(d)} chars (max 155)")
            descs.setdefault(d, []).append(rel)
        if p.h1 != 1:
            errors.append(f"{rel}: has {p.h1} <h1> elements (want exactly 1)")

    for t, where in titles.items():
        if len(where) > 1:
            errors.append(f"duplicate title '{t}' on {', '.join(where)}")
    for d, where in descs.items():
        if len(where) > 1:
            errors.append(f"duplicate description on {', '.join(where)}")

    print(f"Checked {len(pages)} pages in {SITE}/")
    if todos:
        shown = sum(v[0] for v in todos.values())
        hidden = sum(v[1] for v in todos.values())
        print(f"Open TODOs: {shown} shown as yellow markers, {hidden} hidden as HTML comments, on {len(todos)} pages")
        print("  shown hidden  page")
        for k, v in sorted(todos.items()):
            print(f"  {v[0]:5d} {v[1]:6d}  {k}")
    if errors:
        print(f"\n{len(errors)} problem(s):")
        for e in errors:
            print("  - " + e)
        sys.exit(1)
    print("\nNo problems found.")


if __name__ == "__main__":
    main()
