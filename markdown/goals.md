I have given approximate durations for these tasks. I have not given deadlines because how to order them is not at all obvious. Some of that will depend on the whims of mamagement :), and some of it on interdependencies between the different tasks.

# document the model
This should be first, as it will make everything else easier -- reviewing the model with y'all, publishing the model, and even guiding the "testing + bugfix" goal.
## complete the "why" documentation (2 weeks)
In two weeks I believe I can document, if not how everything works, at least what every program does. Filling out those missing details require testing, so would naturally go hand-in-hand with the testing project.
# test + bugfix the model (3 months)
There will be a symbiotic relationship between this and the review and documentation goals.

This never really ends. However, two major milestones would be the following.
## extend tests throughout the entire program (2 months)
## address every known or likely bug (1 month)
See "bugs.pdf".
# review the model with microsimulation team (1.5 weeks)
This will be a good check on the documentation process,
and a good stepping stone toward improving and extending the model.
## iron out the VAT-COICOP bridge
That document is currently kind of a mess. Most of the numbers are 0, 5% or 19%, but there are some weird ones. Some of them (e.g. the extra tax on heavy-duty motorcycles) aren't even VAT. Once we review the model we'll hopefully have some idea what to do about this.
# improve the model process (5 weeks)
## use Vaex to reduce memory load (1 week)
I've ordered more memory for my laptop. Hopefully I'm able to install it, and it will lead my laptop to once again be able to run the model
## homogenize formats upstream (1 week)
Currently data sets are cleaned as needed by downstream code. This is ad-hoc and dangerous -- it causes duplication of code, it's easy to forget why it's there, and it can introduce parse errors that might go uncaught. Better would be to ensure that each data product is in the same format before it is processed at all.
## automate the construction of the raw data (1 week)
Currently it's half-automated, half-manual. This is dangerous, both because I have to get it right every time I redo it (e.g. if my machine were to break), and because someone else would not know what to do if I were to break.
## transition from make to make.py (2 weeks)
The syntax of `make` is a monster. Even I can barely understand what I wrote. Someone else would be totally lost. make.py, by contrast, requires someone to know nothing beyond ordinary Python. It's simpler, cleaner-looking, easier to edit, *and* more expressive.
# serve the model online (3 months)
## BTW, it's $60/month.
I was wrong. A *static* website costs like a dollar per month. That's because you don't need a dedicated processor. A *dynamic* website costs around $60/month, because you've got to keep a processor constantly ready to receive and process user requests.
## Understand how to process user keyboard/mouse input.
I'm close to done with this. I can already do it, in fact, but I have a poor grasp of what I'm doing -- I'm aping other peoples' code, so I'm not quite ready to generalize it to our purposes.
## Learn how to input .xlsx, and how to output .xlsx and .pdf
Haven't done it, but I don't think it's hard.
## Be able to process user input
Some user input will be driven by the web GUI.
Other (particularly providing a new VAT schedule) will be through .xlsx upload.
The code is not currently designed to accept those things in such a flexible way.
This will be tricky.
## Decide what pictures we want to give the user.
They could be displayed on the website but I'd get it done faster if I just return a PDF,
and I think it'd be more useful to the user, too.
## Code the generation of those pictures.
# extend the model
I don't know. What's next? Corporate income tax?
