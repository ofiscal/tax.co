# Git and Github

Git is a version-control system. It's used mostly by coders but you could use it for any kind of text document. Git makes it easy to track when you changed what, keep alternate versions of things, and collaborate.

Github is a place where a lot of people keep their Git repositories.

[The Github website](https://github.com/) provides a friendly introduction to both.


# Python, iPython, and some Python libraries

tax.co is written in [Python](https://www.python.org/).

iPython is a browser-based development environment good for exploring data visually and creating pretty documents. Here is a list of [iPython shortcuts](https://www.webucator.com/blog/wp-content/uploads/2015/07/IPython-Notebook-Shortcuts.pdfa).

[SciPy](https://www.scipy.org/) is a collection of libraries handy for data science.


# Docker and DockerHub

[Docker](https://www.docker.com) is a container system for software. When someone builds a Docker image, anybody with Docker (regardless of what operatinig system they're running) can run that container and expect the same behavior.

[DockerHub](hub.docker.com) is a place where a lot of people keep their Docker images.



# TeX

[TeX](https://www.tug.org/begin.html) is a programming language for document creation. You describe what text and images you want, and it creates a nice-looking PDF for you.

# org-mode

Org-mode is a plain text format resembling markdown,
suitable for highly nested passages. It uses the file extension ".org".
Some of this project's documentation, most notably the TODO list
"org/TODO.org", is written in org-mode.

You can read an org-mode document in any text editor.
However, some editors "understand" it,
allowing you to do clever things like fold nested passages.
Org-mode evolved in the Emacs ecosystem,
and Emacs has the best support for it.

# OBSOLETE: Freeplane

I've ported all the Freeplane documentation to org-mode,
because Freeplane's developers have more or less abandoned it.
I'm only including this description to cover the remote possibility
that you'll want to use it to understand what was happening in an earlier
phase of the project.

[Freeplane](https://www.freeplane.org/wiki/index.php/Home) is an open-source application for mapping knowledge as a tree of foldable natural language objects (words, sentences, paragraphs) called |vertices". It is useful for organizing non-tabular information, such as plans, requirements, or how to use a dataset.


## Installing Freeplane

On Linux it is easily installed via apt; on other operating systems you'll probably have to download a binary or build from source.


## Using Freeplane

Documentation elsewhere makes Freeplane look complicated, but really there are a very small number of commands to know. The key concept is that sometimes you are editing the text within a vertex, and sometimes you are rearranging the vertices in the tree. In either mode, highlight, cut, copy and paste work like they do in most apps.

In tree-mode, up, down, left and right do what you would expect. Spacebar "folds" or "unfolds" a branch of the tree: When a vertex is unfolded you see its children, and maybe their children, etc; when the vertex is folded you see it but not its descendents. Pressing Enter creates a new sibling under the current vertex, and enters text-mode, so you can put text in the new vertex. Pressing Insert creates a new child of the current vertex, and again enters text-mode so you can write in it.

You can also enter text-mode by pressing Home or End. Exit it by pressing Enter. To create a newline within a node, press Shift-Enter.

That's all there is to it!


## Making Freeplane cooperate with Git

Freeplane stores data in a verbose XML format, which can interact badly with a version control system.

The problem is that by default, Freeplane saves a parameter in each vertex indicating whether the vertex is folded or not. Therefore simply viewing the document can appear to change the structure of the document, bloating the size of its history in Git.

The solution is easy: In Preferences, under "Save folding", select "Never". Now save those preferences: click "Save" at the bottom of the Preferences window, name the file something like "options", and leave it in the default path provided (which will be something like "~/.config/freeplane/1.6.x/"). Last, restart Freeplane.
