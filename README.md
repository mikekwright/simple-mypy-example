Testing out mypy
============================

This repo contains some of my experimentation with mypy to see how
well it functions at the current time (July 2019 - version 0.711).  

The main reason that I am spending time on this project is that I have
spent a few years now working with python on the machine learning
research team and have run into a few times when larger code bases start
to cause some typing headache.  

The main two things that I am looking for right now are:

1. How accurate is mypy and how does it handle code that is harder to determine
  typing information
2. Does there seem to be too rigid of a requirement when coding (don't want to give us to much on the python flexibility)

## Experiments

There are going to be a few different scenarios that I am going to craft, these
do not necessarily represent true programming practices, but rather are a way
to test the `mypy` tool with _complex_ code.  

### 1. Start Simple

For the first experiment we are going to just see how it handles a simple
function in a main, and what the output is if it is run with an invalid
argument.  

```python
def test(name: str) -> str:
  print(name)
  return 'what'
```

When attempting to call with `print(test('hi'))` and running `mypy` we get no
output and a return code of 0 (a good sign).  

However, lets see what we get when we change to `print(test(1))`:

```bash
  |15:21:00| ~/Development/personal/simple-mypy-example $ mypy main.py 
main.py:8: error: Argument 1 to "test" has incompatible type "int"; expected "str"
```

So it looks like it caught the issue however running the program using python
still works just fine.  

### 2. Multiple Functions

For this next experiment we are going to see how the mypy tool works when multiple
functions are created and attempted to be called directly and also when held in 
a common variable.  

```python
def first(x: str) -> str:
    return f'first {x}'

def second(y: int) -> str:
    return f'second {y}'
```

If we have a `__main__` that calls the functions directly it works as expected
from the first experiment.  

Lets try a little more complex version that will use `random` and assign a function
to a variable and attempt to call it.  

```python
if __name__ == '__main__':
    x = first if random.random() > 0.5 else second
    print(x('hi'))
```

It seems that mypy will correctly handle this situation by informing us that
there is an unknown type.  

```bash
 [127] |15:29:26| ~/Development/personal/simple-mypy-example $ mypy main.py
main.py:11: error: Cannot call function of unknown type
```

Hmm, alright well lets try to make this a bit harder by actually storing
the functions in a list and selecting the function to use from the list
instead of name directly.  

```python
if __name__ == '__main__':
    funcs = [first, second]
    x = funcs[0] if random.random() > 0.5 else funcs[1]
    print(x('hi'))
```

So, this triggers the same error output:  

```bash
  |15:31:36| ~/Development/personal/simple-mypy-example $ mypy main.py 
main.py:12: error: Cannot call function of unknown type
```

So the next step was to see if I could apply a type to the variable:

```python
expression has type "function", variable has type "Callable[..., Any]
```

However, this also ended in an error, but not the error I would have expected:

```bash
 [1] |15:40:44| ~/Development/personal/simple-mypy-example $ mypy main.py 
main.py:14: error: Incompatible types in assignment (expression has type "function", variable has type "Callable[..., Any]")
```

This is a rather odd error, so I am going to see if there is a way to define
the variable in the list first and if that will resolve the issue.  

```python
if __name__ == '__main__':
    funcs = [first, second]  # type: List[Callable[..., str]]
    x = funcs[0] if random.random() > 0.5 else funcs[1]
    print(x('hi'))
```

That seems to have resolved the issue, although it isn't catching the entire issue
but that is likely because I was generic in my `Callable`, allowing it to take in
an arbitrary list of arguments (`...`).  

So, I can make some other changes that will make it smarter, but it looks like once
I have made this more generic to specific there is nothing that forces that.  For
example in this below example, I am saying the type of the output should be a
`Callable[[str], str]`, however the list that holds the callables just has the
type of `List[Callable[..., str]]`.  This does not end in an error, but instead
it says that everything is good.  

```python
if __name__ == '__main__':
    funcs = [first, second]  # type: List[Callable[..., str]]
    x = funcs[0] if random.random() > 0.5 else funcs[1] # type: Callable[[str], str]
    print(x('hi'))
```

## Conclusion

This repo was used for a quick view of `mypy` and to see how it worked when placed
in some rather difficult scenarios to determine types.  Outside of the comment
driven variable type support, the tool worked pretty well from the two little
experiments that I played with.  I am planning to, moving forward, use `mypy` in
a simple project to see how well it works in a larger real world example.  
