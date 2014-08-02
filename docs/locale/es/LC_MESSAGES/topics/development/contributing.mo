��                          �     9   �     �  l   �  V   f     �  	  �     �  *   �  F     �   f  �   T  6   �  b        q     �  �   �    m  =   u	  K   �	  @   �	  �   @
  �   1  a   �          :  �  A  �   �  �   X  w  �  }  e  �   �  9   �     �  l   �  V   <     �  	  �     �  *   �  F   �  �   <  �   *  6   �  b   �     G     e  �   �    C  =   K  K   �  @   �  �     �     a   �     �       �    �   �  �   .  w  �   By signing-off you indicate that you are accepting the Developer Certificate Of Origin. For now, we are using them same DCO as `Linux kernel developers are using`_. Choose a name for your branch that describes its purpose. Contributing First, make a local clone of your GitHub fork of the L.I.S.A GitHub repo and make edits and changes locally. For more info, see `GitHub Fork a Repo Guide`_ or `Open Comparison Contributing Docs`_ Keeping L.I.S.A Forks in Sync L.I.S.A is advancing quickly. It is therefore critical to pull upstream changes from master into forks on a regular basis. Nothing is worse than putting in a days of hard work into a pull request only to have it rejected because it has diverged too far from master. Minor releases Minor releases normally contain bug fixes. Now commit your changes to this new branch with the following command: Now go look at your fork of the L.I.S.A repo on the GitHub website. The new branch will now be listed under the "Source" tab where it says "Switch Branches". Select the new branch from this list, and then click the "Pull request" button. Pull requests that are accepted to L.I.S.A but not merged into a minor release will always be available in the next major release. Push your locally-committed changes back up to GitHub: Put in a descriptive comment, and include links to any project issues related to the pull request. Sending a GitHub pull request Sign off your pull request The following is an example (from `Open Comparison Contributing Docs`_ ) of an efficient workflow for forking, cloning, branching, committing, and sending a pull request for a GitHub repository. The repo managers will be notified of your pull request and it will be reviewed. If a reviewer asks for changes, just make the changes locally in the same local feature branch, push them to GitHub, then add a comment to the discussion section of the pull request. Then to accept the changes and merge into the current branch: Then, create a new branch on your clone by entering the following commands: There are a number of ways to contribute to L.I.S.A development. There is a great need for contributions to L.I.S.A and patches are welcome! The goal here is to make contributions clear, make sure there is a trail for where the code has come from, and most importantly, to give credit where credit is due! This is the preferred method for contributions. Simply create a GitHub fork, commit changes to the fork, and then open up a pull request. To check the log to be sure that you actually want the changes, run the following before merging: To pull in upstream changes: Travis Using ``git commit -am``, followed by a quoted string, both stages and commits all modified files in a single command. Depending on the nature of your changes, you may wish to stage and commit them separately. Also, note that if you wish to add newly-tracked files as part of your commit, they will not be caught using ``git commit -am`` and will need to be added using ``git add`` before committing. When making pull requests, please sign-off the pull request in a pull request comment. You can simply make a comment something like:: When submitting a pull-request which should be considered for a minor release, please note in the comments that it should be reviewed for inclusion. Whenever you make a pull request against the main L.I.S.A repository your changes will be tested. On average these tests take few minutes to run and once they are complete a PASS/FAIL message will be added to your pull request. This message contains a link to https://www.travis-ci.org where you can review the test results. This message will also generate an email which will be sent to the email address associated with your GitHub account informing you of these results. It should be noted that a test failure does not necessarily mean there is an issue in the associated pull request as the entire development branch is tested. Project-Id-Version:  LISA
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2014-06-01 08:27+0200
PO-Revision-Date: 2014-06-01 06:27+0000
Last-Translator: Julien Syx <nephilim.seraphin@gmail.com>
Language-Team: Spanish (http://www.transifex.com/projects/p/lisa/language/es/)
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 1.3
 By signing-off you indicate that you are accepting the Developer Certificate Of Origin. For now, we are using them same DCO as `Linux kernel developers are using`_. Choose a name for your branch that describes its purpose. Contributing First, make a local clone of your GitHub fork of the L.I.S.A GitHub repo and make edits and changes locally. For more info, see `GitHub Fork a Repo Guide`_ or `Open Comparison Contributing Docs`_ Keeping L.I.S.A Forks in Sync L.I.S.A is advancing quickly. It is therefore critical to pull upstream changes from master into forks on a regular basis. Nothing is worse than putting in a days of hard work into a pull request only to have it rejected because it has diverged too far from master. Minor releases Minor releases normally contain bug fixes. Now commit your changes to this new branch with the following command: Now go look at your fork of the L.I.S.A repo on the GitHub website. The new branch will now be listed under the "Source" tab where it says "Switch Branches". Select the new branch from this list, and then click the "Pull request" button. Pull requests that are accepted to L.I.S.A but not merged into a minor release will always be available in the next major release. Push your locally-committed changes back up to GitHub: Put in a descriptive comment, and include links to any project issues related to the pull request. Sending a GitHub pull request Sign off your pull request The following is an example (from `Open Comparison Contributing Docs`_ ) of an efficient workflow for forking, cloning, branching, committing, and sending a pull request for a GitHub repository. The repo managers will be notified of your pull request and it will be reviewed. If a reviewer asks for changes, just make the changes locally in the same local feature branch, push them to GitHub, then add a comment to the discussion section of the pull request. Then to accept the changes and merge into the current branch: Then, create a new branch on your clone by entering the following commands: There are a number of ways to contribute to L.I.S.A development. There is a great need for contributions to L.I.S.A and patches are welcome! The goal here is to make contributions clear, make sure there is a trail for where the code has come from, and most importantly, to give credit where credit is due! This is the preferred method for contributions. Simply create a GitHub fork, commit changes to the fork, and then open up a pull request. To check the log to be sure that you actually want the changes, run the following before merging: To pull in upstream changes: Travis Using ``git commit -am``, followed by a quoted string, both stages and commits all modified files in a single command. Depending on the nature of your changes, you may wish to stage and commit them separately. Also, note that if you wish to add newly-tracked files as part of your commit, they will not be caught using ``git commit -am`` and will need to be added using ``git add`` before committing. When making pull requests, please sign-off the pull request in a pull request comment. You can simply make a comment something like:: When submitting a pull-request which should be considered for a minor release, please note in the comments that it should be reviewed for inclusion. Whenever you make a pull request against the main L.I.S.A repository your changes will be tested. On average these tests take few minutes to run and once they are complete a PASS/FAIL message will be added to your pull request. This message contains a link to https://www.travis-ci.org where you can review the test results. This message will also generate an email which will be sent to the email address associated with your GitHub account informing you of these results. It should be noted that a test failure does not necessarily mean there is an issue in the associated pull request as the entire development branch is tested. 