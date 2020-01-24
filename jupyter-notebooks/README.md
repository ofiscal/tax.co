# Why

This code isn't necessary, but it might be convenient. Jupyter is an environment accessible from the browser that offers a graphical REPL. The effects of changes to code that generates pictures can be viewed quickly, without needing to switch contexts.

# How

From the docker container, type `cd` to go to the home folder (which is `/root/`). From there, execute `bash run-jupyter.sh`. Some messages will print to the screen, among them some URLs. Try pasting one of the URLs into a browser. You should now see a list of the contents of the folder that the Docker container was mounted to. You can navigate within that (but not outside of it), open any Jupyter notebooks therein (they end in `.ipynb`), or create new ones.
