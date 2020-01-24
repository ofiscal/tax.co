This describes the branches the code has gone through, in the [git sense of the word](https://git-scm.com/docs/git-branch).

# safe-strings

The purpose of this branch was to assign each column name (and in the case of categorical variables, each column value) to a variable, and then use that variable instead of the raw string. But once I could see what that's like, I decided it's actually no safer -- it creates some boilerplate that could be hard to maintain, and requires a lot of tedious definitions that can be more easily handled with regular expressions (e.g. in build.people.main).
