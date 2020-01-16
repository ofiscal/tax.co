I have given approximate durations for these tasks. For all but one, I have not given deadlines, because how to order them is not at all obvious. Some of that will depend on the whims of mamagement :), and some of it on interdependencies between the different tasks.

# GOAL: Document the model
This should be first, as it will make everything else easier -- reviewing the model with y'all, publishing the model, and even guiding the "testing + bugfix" goal.

## Complete the "why" documentation (2 weeks -- February 1)
In two weeks I believe I can document, if not how everything works, at least what every program is intended to accomplish. Filling out those missing details require testing, so would naturally go hand-in-hand with the testing project.

(There's some exploratory code which I'm hanging onto even though I doubt anyone I will ever be able to use it, and surely never anyone else; I won't document that stuff any more than it already is.)

Other duration estimates in this document could well change as an effect of completing this step. For instance I'll have a much clearer idea of how much work it will be to test the rest of the build chain.

# GOAL: Test + bugfix the model (3 months)
There will be a symbiotic relationship between this and the review and documentation goals.

This never really ends. However, two major milestones would be the following.

## Extend tests throughout the entire program (2 months)

That's my intuitive sense. Once I document the code I'll be able to break down this task in detail.

## Address every known or likely bug (1 month)
They are listed in `bugs.md.pdf`.

# GOAL: Review the model with microsimulation team (1.5 weeks)
This will be a good check on the documentation process,
and a good stepping stone toward improving and extending the model.

## Iron out the VAT-COICOP bridge
The bridge is currently kind of a mess. Most of the numbers are 0, 5% or 19%, but there are some weird ones. Some of them (e.g. the extra tax on heavy-duty motorcycles) aren't even VAT. Once we review the model we'll hopefully have some idea what to do about this.

# GOAL: Improve the model process (5 weeks)

On the one hand, I'd like to test before making these improvements, because as soon as someone asks us to do something with the model, the tests become really important. On the other, if I did this first, it would reduce the total amount of time spent coding, because (a) the code will be cleaner, hence easier to test, and (b) I won't have to modify any existing tests for these new methods if I only write the tests after putting these changes in place.

## Use Vaex to reduce memory load (1 week)
I've ordered more memory for my laptop. Hopefully I'm able to install it, and it will lead my laptop to once again be able to run the model

## Homogenize formats upstream (1 week)
Currently data sets are cleaned as needed by downstream code. This is ad-hoc and dangerous -- it causes duplication of code, it's easy to forget why it's there, and it can introduce parse errors that might go uncaught. Better would be to ensure that each data product is in the same format before it is processed at all.

## Automate the construction of the raw data (1 week)
Currently it's half-automated, half-manual. This is dangerous, both because I have to get it right every time I rebuild the data (rare, but it does happen), and because it will reduce the cognitive load on any hypothetical newcomer to the team.

## Transition from make to make.py (2 weeks)
What `make` does is wonderful, but its syntax is a minefield -- brittle to changes, full of pitfalls that can result in silent errors, hard to read. Even I often have trouble understanding what I wrote. Someone else would probably be in a world of hurt. `make.py`, by contrast, requires someone to know nothing beyond ordinary Python. It's simpler, cleaner-looking, easier to edit, more reliable, *and* more expressive.

# GOAL: Serve the model online (3 months)

## BTW, hosting an active site on AWS costs more like $60/month.
I was wrong. A *static* website costs like a dollar per month. That's because you don't need a dedicated processor standing by. A *dynamic* website costs around $60/month, because it's got to stay constantly ready to receive and process user requests.

Alternatives to AWS can be up to four times cheaper. AWS offers literally dozens of services; "bare metal providers", by contrast, just give you a machine. Most of my learning investment has been in Django, the web framework for building sites, which is portable across cloud providers. Switching from AWS to a cheaper service might cost me two weeks to get up to date. There might however be reliability problems that AWS doesn't suffer from.

## Understand how to process user keyboard/mouse input.
I'm close to done with this. I can already do it, in fact, but I have a poor grasp of what I'm doing -- I'm aping other peoples' code, and not quite ready to generalize it to our purposes.

## Learn how to input .xlsx, and how to output .xlsx and .pdf
Haven't done it, but I don't think it's hard.

## Be able to process user input
Some user input will be driven by the web GUI.
Other (particularly providing a new VAT schedule) will be through .xlsx upload.
The code is not currently designed to accept those things in such a flexible way.

This will be the lion's share of the port-to-cloud job.

## Decide what pictures we want to give the user.
They could be displayed on the website but I'd get it done faster if I just return a PDF,
and I think it'd be more useful to the user, too.

Pretty easy.

## Code the generation of those pictures.

Pretty easy.

# GOAL: Extend the model
I don't know. What's next? Corporate income tax?
