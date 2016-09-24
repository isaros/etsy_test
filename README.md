# Finding Significant Terms

An Etsy Data Science recruitment homework assignment.

## Overview

This is a two-part test of general coding skills, with a data mining/NLP slant.

We provide two sets of Etsy listing IDs. In the first part, you must download all the corresponding listing titles from our public API. In the second part, you must produce a list of the top 100 most discriminative terms, i.e. the ones that would be most helpful for a learning algorithm trying to distinguish the two sets of listings. More details on each part are provided below.

## Requirements
* python 2.7

## How to Run the program
* `cd etsy_test/app`
* For only the data processing `python -m data_processing`
* For only the data mining `python -m data_mining`
* For the whole process `python -m __main__`

## Test
* `cd etsy_test`
* `python -m test.test`

## Solution

I choose to divide the work in two parts:
* First the data fetching and processing
    * The IDs from the file are read and stored in a list before be use to fetch the information through the API
    * Iterations on the ID list is processed and the API is called by batches on its limit of resource (i.e 100 resources at a time).
    * The result is a the same time decoded processed and clean before being stored
    * Eventually we iterate over the titles list to save then in a file.

    I decided not to save in the file at every iteration but only at the end because I though that this part of the program (the output lists) could be directly given to the data mining part. In case we don't want to handle files in between. But in the given solution that reduce the performance of the program.
* Then the data mining part :
    * Everything is explained in detail in the code. But the general idea is to find a measure of how discriminatory a feature (here a token) is. Which means how this feature help me to distinguish between class A and class B. For that we use the very classic idea of entropy in information theory.
    * It would be interesting to see now the importance of these top 100 features to distinguish the class A or B. And then build a decision tree using these feature to do prediction afterwards.

# Context of the solution

### The word list

This should be a text file called `results.txt` with 100 terms, one on each line, in descending order of discriminative power. See the detailed instructions on part 2 below to understand what we mean by that.

## Restrictions

Please use one of the following languages: Java, Scala or Python. You can use different languages for part 1 and part 2 if you like.

**Don't** use any third-party libraries beyond those which are provided with your chosen language's standard library. **Exception:** If you are using Java or Scala for part 1, you may use a third-party library for HTML entity decoding, since there isn't a method for this in the JDK or Scala standard library.

Your code must compile (if applicable) and run on a typical Mac or Linux machine without modification. Our developer machines use JDK 7 and 8, Scala 2.10 and Python 2.7 as standard, so please target one of these versions.

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
