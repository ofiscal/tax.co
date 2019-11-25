from itertools import chain


files = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" ]
samples = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

def rules(ctx):
  natural(ctx)
  fast(ctx)

def natural(ctx):
  targets = [ "natural/" + s + "/" + f
              for s in samples
              for f in files ]
  ctx.add_rule(
    targets,
    [ "input/" + f
      for f in files ],
    [ [ "cp", "input/" + f, "natural/" + s ]
      for s in samples
      for f in files ] )

def fast(ctx):
  big_target = "fast/phony"
  ctx.add_rule(
    big_target,
    [ "input/" + f
      for f in files ],
    ( list( # turn the chain.iterable into a list
        chain.from_iterable( # concatenate the lists
          [ [ [ "mkdir", "-p", "fast/" + s ],
            [ "cp", "input/" + f, "fast/" + s ] ]
          for s in samples
          for f in files ] ) )
      + [["touch", big_target]] ) )

  for s in samples:
    for f in files:
      small_target = "fast/" + s + "/" + f
      ctx.add_rule(
        small_target,
        [ big_target ],
        [ "touch", small_target ] ) # without this `touch`, `target`
               # would look out of date relative to its dependencies
