********************
Developer Guidelines
********************

Git Repository
===============

Layout
------

The git repository is structured by a number of branches and clones (forks) at
github_.
Anyone is welcome to fork the repository on github_ (just click on "Fork"
button), and file a "Pull request" whenever he/she thinks that his changes are
ready to be included (merged) into the main repository.

.. _github: https://github.com/BNUCNL/FreeROI

Branches
--------

Theoretically, any developer can have an infinite number of branches.

The main release branch is called *master*.  This is a merge-only branch.
Features finished or updated by some developer are merged from the
corresponding branch into *master*.  At a certain point the current state of 
*master* is tagged -- a release is done.

Only usable feature should end-up in *master*.  Ideally *master* should be
releasable at all times.  Something must not be merged into master if *any*
unit test fails.

Commits
-------

Please prefix all commit summaries with one (or more) of the following labels.
This should help others to easily classify the commits inti meaningful
categoroes:

  * *BF* : bug fix
  * *RF* : refactoring
  * *NF* : new feature
  * *ENH* : enhancement of an existing feature/facility
  * *BW* : address backward-compatibility
  * *OPT* : optimization
  * *BK* : breaks someing and or tests fail
  * *PL* : making pylint happier
  * *DOC* : for all kinds of document related commits
