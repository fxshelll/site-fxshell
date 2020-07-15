---
title: "Rust Idioms"
date: 2019-11-03T13:23:12-06:00
draft: false
---

# Resources
Below are some great resource that were used for this page:

* Rust Programming Techniques: https://youtu.be/vqavdUGKeb4
* Rust Language Cheat Sheet: https://cheats.rs/

# Pattern Matching
```rust
enum Foo {
    A(i32),
    B,
    C
}

let foo = match x {
    Foo::A(n) => n,
    _ => 0,
};
```

## Option Type
```rust
enum Option<T> {
    Some(T),
    None
}
```

## Result Type
```rust
enum Result<T, E> {
    Ok(T),
    Err(E)
}
```
Example:
```rust
fn h(value: i32) -> Result<i32, String> {
    match i {
        i if i >= 0 => Ok(i + 10),
        _ => Err(format!("Input to h less than 0, found {}", i))
    }
}

fn main() {
    let input: i32 = 4;
    match h(input) {
        Ok(value) => println!("Result: {}", value),
        Err(e) => println!("Error: {}", e)
    }
}
```

## if let
```rust
if let Ok(i) = h() {
    // do something
}
```
We ignore any error.

## ?
Common idiom:
```rust
let i = match h() {
    Ok(i) => i,
    err => return err  // throw the error
};
```
Equals to the following one liner:
```rust
let i = h()?;
```

## map (some method)
```rust
fn add_four(x: i32) -> i32 {
    x + 4
}

fn maybe_add_four(y: Option<i32>) -> Option<i32> {
    match y {
        Some(yy) => Some(add_four(yy)),
        None => None
    }
}
```
Use of map:
```rust
fn add_four(x: i32) -> i32 {
    x + 4
}

fn maybe_add_four(y: Option<i32>) -> Option<i32> {
    y.map(add_four)
}
```
Clojure form:
```rust
fn maybe_add_four(y: Option<i32>) -> Option<i32> {
    y.map(|x| x + 4)
}
```

## and_then, filter
"Idiomatization" (🤔...) of the following:
```rust
fn foo(input: Option<i32>) -> Option<i32> {
    if input.is_none() {
        return None;
    }
    let input = input.unwrap();
    if input < 0 {
        return None;
    }
    Some(input)
}
```
Use of "?":
```rust
fn foo(input: Option<i32>) -> Option<i32> {
    let input = input?;  // return None if None
    if input < 0 {
        return None;
    }
    Some(input)
}
```
Use of `and_then`:
```rust
fn foo(input: Option<i32>) -> Option<i32> {
    input.and_then(|i| {
        if i < 0 {
            None
        } else {
            Some(i)
        }
    }
}
```
Use of `filter`:
```rust
fn foo(input: Option<i32>) -> Option<i32> {
    input.filter(|i| i >= 0);
}
```

## ok_or
"Idiomatization" (🤔...) of the following:
```rust
fn bar(input: Option<i32>) -> Result<i32, ErrNegative> {
    match foo(input) {
        Some(n) => Ok(n),
        None => ErrNegative
    }
}
```
```rust
fn bar(input: Option<i32>) -> Result<i32, ErrNegative> {
    foo(input).ok_or(ErrNegative)
}
```

# Iterators

```rust
fn ping_all(foos: &[Foo]) {
    for f in foos {
        f.ping();
    }
}
```
Becomes
```rust
fn ping_all(foos: &[Foo]) {
    foos.iter().for_each(|f| f.ping());
}
```

## map, filter, for_each methods
```rust
let vec = vec![0, 1, 2, 3];
vec.iter()
   .map(|x| x + 1)
   .filter(|x| x > 1)
   .for_each(|x| println!("{}", x));
```

## chain, enumerate methods
```rust
let vec = vec![0, 1, 2, 3];
for (i, v) in vec.iter()
                  .chain(vec![4, 5, 6, 7].iter())
                  .enumerate() {
    // do something
}
```
`chain` adds an iterator to an iterator.

## collect method
```rust
let vec = vec![0, 1, 2, 3];
let vec_2: Vec<_> = vec.iter().map(|x| x + 2).collect();
let map: HashMap<_, _> = vec.iter()
                            .map(|x| x * 2)
                            .enumerate()
                            .collect();
```
`_` is used to let the compiler infer the type for us.
Type declarations (`Vec`, `HashMap`) are explicitely needed though to help `collect` to figure out what needs to be returned.
