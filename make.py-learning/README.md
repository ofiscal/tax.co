# What this is

I posted [an issue](https://github.com/zwegner/make.py/issues/5) to github/make.py because I thought I had to do something awkward to get a recipe to run fast. He asked for a minimal example. This is it.

But once I made a minimal example, the problem disappeared. So now I have to figure out the sense in which this is not what my non-minimal example (the actual rules.py file for tax.co) is doing.

# How to use this

From this folder, run

```bash
mkdir input
for i in {a..z}; do echo $i > input/$i; done
```

Then try running commands like these:

* `make.py natural/1/a`
* `make.py natural/10/z`
* `make.py fast/1/a`
* `make.py fast/phony`
