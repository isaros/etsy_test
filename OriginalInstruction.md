# Finding Significant Terms

An Etsy Data Science recruitment homework assignment.

## Overview

This is a two-part test of general coding skills, with a data mining/NLP slant.

We provide two sets of Etsy listing IDs. In the first part, you must download all the corresponding listing titles from our public API. In the second part, you must produce a list of the top 100 most discriminative terms, i.e. the ones that would be most helpful for a learning algorithm trying to distinguish the two sets of listings. More details on each part are provided below.

This exercise should take you less than a day. If you feel that it's likely to take a day or more to complete, please wrap up sooner, and leave comments indicating which parts need completing or finessing. We don't want you to waste days on this!

Please read all the following instructions carefully.

## What to provide

We'd like to see the following things, archived into a zip or tar.gz file:

### A readme file (text or markdown)

This should cover:

* How to compile (if applicable) and run your program(s)
* How your solution works, at a high level
* Why you chose this approach in particular
* What drawbacks there are with this approach, if any

Don't go overboard -- a few paragraphs of text is fine, but make sure the instructions are clear.

### The word list

This should be a text file called `results.txt` with 100 terms, one on each line, in descending order of discriminative power. See the detailed instructions on part 2 below to understand what we mean by that.

### Your solution's source code

Remember to provide the source code for both parts 1 and 2, even though you don't need to provide the output data from part 1.

**Note:** If you prefer, you can submit a single program that tackles both part 1 and part 2. But we would recommend tackling the two parts separately, and writing the output from part 1 to a temporary file. Otherwise you will need to re-download the data each time.

If there are places in your code where you would have made an improvement, given more time, please add a comment to say so. Then at least we know you considered this option.

## Restrictions

Please use one of the following languages: Java, Scala or Python. You can use different languages for part 1 and part 2 if you like.

**Don't** use any third-party libraries beyond those which are provided with your chosen language's standard library. **Exception:** If you are using Java or Scala for part 1, you may use a third-party library for HTML entity decoding, since there isn't a method for this in the JDK or Scala standard library.

Your code must compile (if applicable) and run on a typical Mac or Linux machine without modification. Our developer machines use JDK 7 and 8, Scala 2.10 and Python 2.7 as standard, so please target one of these versions.

## Assessment criteria

You will be assessed on the following criteria:

* Following the instructions!
* Correctness of top term list
* Solution design
* Efficiency of chosen algorithms
* Code quality, style and presentation
* Clarity of documentation (i.e. readme and code comments)

Please write as if you were developing code for yourself and others to maintain, not a throwaway hack to generate a one-off set of results. We want to see what you'd be like to work with, in the long term.

Note that if your solution produces a completely wrong top term list, the chances are that we won't even bother looking at the source code, so it's important to get this right.

## Instructions

### Before you start

Go to the Etsy Developers site and register an app to obtain an API key:

https://www.etsy.com/developers/documentation/

Call your app something like "Etsy Data Science homework for YOUR NAME HERE" -- it doesn't matter too much, you just need an API key (sometimes called a "keystring") so you can access listing data via our API.

### Part 1: data collection

The files `listings_A.txt` and `listings_B.txt` contain two distinct sets of listing IDs for items sold on Etsy. We'll call these listings class A and class B.

For each of these listings, you must connect to the Etsy API (see the documentation linked above), retrieve the corresponding JSON listing record, and extract the `title` field.

Then perform the following cleaning/preprocessing steps on each title:

* Decode any html entities
* Convert all characters to lowercase
* Replace any backslashed characters (e.g. "\n") with a single space
* Remove any leading or trailing non-alphanumeric characters from *each* token
  * Any tokens containing *only* non-alphanumeric characters should be ignored
* Replace any runs of whitespace with a single space

For example, the following made-up title:

    Purple &quot;unicorn-hair&quot; sweater!\nAmaze  all your friends.

Would become:

    purple unicorn-hair sweater amaze all your friends

We recommend that you then save the resulting processed titles out to two text files, one title per line, e.g. `titles_A.txt` and `titles_B.txt`. However, you *won't* be marked on the contents of these files, so don't feel obliged to provide them.

#### Important notes

1. Some listings may be unavailable, e.g. if they have sold or expired. In these cases, the record returned by the API will not contain a `title` field. Just ignore these ones.
2. Be aware of non-ASCII characters in the results -- you may need to use a unicode-friendly encoding such as UTF-8 if you write the data out to a file.
3. Be aware of our API rate limits: https://www.etsy.com/developers/documentation/getting_started/api_basics

There should be more than enough requests available per day to complete this task, and you can request multiple listings in one request to reduce usage. However, there are also hourly and per-second limits to take into account. Read the docs carefully.

### Part 2: data mining

In part 2, the objective is to identify the tokens from these processed titles which are most useful in distinguishing the two classes of listing.

The idea is that each token `t` can be used as a *feature* or *attribute* by which you can split the original population (classes A and B together) into two subsets: those which contain `t`, and those which don't contain `t`.

Intuitively, we'll need a measure of how discriminative `t` is -- that is, how pure the resulting subsets are. If `t` has high discriminatory power, you'd expect one subset to be mostly from class A and the other to be mostly from class B. On the other hand, if `t` has low discriminatory power, both subsets will have a blend of class A and class B listings.

In order to do this, we'll use the concept of information gain, as described (for example) here:

http://homes.cs.washington.edu/~shapiro/EE596/notes/InfoGain.pdf

or here:

http://stackoverflow.com/a/1859910

A term with high information gain has high discriminatory power.

Conceptually, the process goes as follows:

* For each token `t`:
  * Split the original population into two subsets:
    * Subset `s1` is all those listings whose titles contain `t`
    * Subset `s2` is all those listings whose titles don't contain `t`
  * Calculate the information gain associated with this split
* Rank the tokens by descending order of information gain
* Output the top 100 tokens to a file

The actual implementation of your algorithm does not need to follow these steps exactly, as long as the results (the tokens and their ordering) are correct.

#### Important notes

1. We don't care about the *number* of times `t` appears in each title, just its presence or absence.
2. The information gain should be calculated with respect to the entire population (class A and B together) each time. That is, you are *not* applying splits in some particular order, as if you were building a decision tree.
3. Don't worry about including the actual information gain scores in the output file. Just provide a list of tokens in *descending* order of information gain, for example:

```
unicorn-hair
ambergris
sparkles
amazeballs
...
teal
```

In this case, `unicorn-hair` is the most powerful discriminator, and `teal` is the 100th most powerful.

