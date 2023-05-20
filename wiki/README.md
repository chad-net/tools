# Chadnet System Alpha: Wiki System

This is used to build the wiki category and search pages from the `db.chad` and
`cat.chad` files in the main directory.

When run, it searches for database files in `../../`, which is one level above
the `tools/` folder.

So, if you use this code it is **crucial** you have it in the proper structure:
`main_wiki_dir_whatever/tools/wiki/`

This code is designed to work for our system. If you want to modify these
locations, see the `constants/paths.py` file.

## How to run

Go back to the tools folder and see the `wiki.sh` file.

**NOTE: ONLY RUNS ON LINUX OR MACOS.**

## What does it do?

1. Backs up the `db.chad` and `cat.chad` files in the `../backups/` folder.

2. Sorts the databases using either the `natsort` package or our own local
version which is slightly faster. The sorting is meant to be akin to GNU's
`sort` program, something which sorts numbers, etc. properly in a way that
makes sense to readers.

3. Overwrites the original database with the sorted one.

4. Updates the `../../index.html` file with the new link count and update time.

5. Creates all the category pages, which consist of a link count, starred links
(new functionality), categories, links, etc.

6. Sets up the search page, which is designed to work offline as well.

7. Changes all file permissions in the `../../wiki/` folder to 644 (skipping
the `../tools/` folder). Does the same in `../../wiki/files/`. Changes the
permissions of the files directory itself to 755.

8. Prints statistics: link count, category count, and execution time.

You can optionally enable debug mode in `constants/options.py`, which creates a
folder `debug/`, where call times, etc. can be analyzed.

## Future additions

Unit tests need to be added.

Functionality will be extended, so this can be used to process the database
files too perhaps (search for individual records, etc.).
