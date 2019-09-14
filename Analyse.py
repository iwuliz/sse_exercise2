# Created by Wuli.Zuo a 1785343
# 9/Sep/2019

from git import Repo, RemoteProgress
import os
import re

# Function of git commands to analyse commits

def git_analyse(local_link, fixing_commit):

    # Create repo object
    repo = Repo(local_link)

    # Reset to given commit
    output_0 = repo.git.reset('--hard', fixing_commit)
    print("Current fix commit: %s" % output_0)
      
    # Question a: get commit message and title
    output_a = repo.git.log(-1, '--format=%B')
    print("\n(a). Commit message and title: %s" % output_a)

    # Question b: get number of affected files
    output_b = repo.git.show('--name-only', '--format=').splitlines()
    print("(b). Number of affected files: %d" % len(output_b))
    
    # Question c: get number of affected directories
    output_c = repo.git.show('--dirstat', '--format=').splitlines()
    print("(c). Number of affected directories: %d" % len(output_c))
    
    # Question d: get number of deleted lines (including comments and blank lines)
    lines = repo.git.show().splitlines()
    output_d = [line for line in lines if re.compile('^-[^-]|^-\s*$').match(line)]
    print("(d). Number of deleted lines (including comments and blank lines): %d" % len(output_d))

    # Question e: get number of added lines (including comments and blank lines)
    lines = repo.git.show().splitlines()
    # lines start with '+', but not followed by '+'
    output_e = [line for line in lines if re.compile('^\+[^\+]|^\+\s*$').match(line)]
    print("(e). Number of added lines (including comments and blank lines): %d" % len(output_e))

    # Question f: get number of deleted lines (excluding comments and blank lines)
    lines = repo.git.show().splitlines()
    # lines start with '-', but not followed by '-'; excluding /*, *, */, //
    lines = [line for line in lines if re.compile('^-[^-]|^-\s*$').match(line)]
    lines = [line for line in lines if not re.compile('^-\s*\/').match(line)]
    lines = [line for line in lines if not re.compile('^-\s*\*').match(line)]
    output_f = [line for line in lines if not re.compile('^-\s*$').match(line)]
    print("(f). Number of deleted lines (including comments and blank lines): %d" % len(output_f))

    # Question g: get number of added lines (excluding comments and blank lines)
    lines = repo.git.show().splitlines()
    # lines start with '+', but not followed by '+'; excluding /*, *, */, //
    lines = [line for line in lines if re.compile('^\+[^\+]|^\+\s*$').match(line)]
    lines = [line for line in lines if not re.compile('^\+\s*\/').match(line)]
    lines = [line for line in lines if not re.compile('^\+\s*\*').match(line)]
    output_g = [line for line in lines if not re.compile('^\+\s*$').match(line)]
    print("(g). Number of added lines (including comments and blank lines): %d" % len(output_g))

    # Question h: number of days between two commit
    print("(h). Number of days between the current fixing commit and the previous commit: ")
    for file in repo.git.show('--name-only', '--format=').splitlines():
        # Check if a file is a new added file in current commit
        output_h = repo.git.log(-2, '--format=%ct', file).splitlines()
        if(len(output_h) == 1):
            print("     This is a new added file.")
        else:
        # convert unit from seconds to days
            print("     %s: %d" % (file, (round(int(output_h[0])-int(output_h[1]))/(60*60*24))))

    # Question i: number of times each affected file has been modified
    print("(i). Number of times each file has been modified: ")
    for file in repo.git.show('--name-only', '--format=').splitlines():
        output_i = repo.git.log('--follow', '--format=oneline', file).splitlines()
        print("     %s:  %d" % (file, len(output_i)))

    # Question j: developers who have modified each file
    print("(j). Developers who have modified each file: ")
    for file in repo.git.show('--name-only', '--format=').splitlines():
        print("     Developers who have modified file: %s " % file)
        authors = repo.git.log('--follow', '--format=%aN', file).splitlines()
        for author in set(authors):
            print("       %s"%author)

    # Question k: number of commits each developer has made
    print("(k). Number of commits each developer has made: ")
    authors = set()
    for file in repo.git.show('--name-only', '--format=').splitlines():
        authors.update(repo.git.log('--format=%aN', file).splitlines())
    authors = list(authors)
    authors.sort()
    for author in authors:
        print("     %s: %d" % (author, len(re.findall(author,repo.git.log('--format=%aN')))))

# main

class Progress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line)

# Case 1
# As mentioned in Exercise 1,
# a complete fix to the vulnerability is provided by combining the provided commit and identified commit together,
# so both commits are analysed here.
remote_link = "https://github.com/spring-projects/spring-amqp"
local_link = "../spring-amqp"
if not os.path.isdir(local_link):
    Repo.clone_from(remote_link, local_link, progress=Progress())
# Analyse the provided commit
fixing_commit_provided = "444b74e95bb299af5e23ebf006fbb45d574fb95"
print("Analyses of repo: %s, commit: %s" % (remote_link, fixing_commit_provided))
# Analyse the identified commit
git_analyse(local_link, fixing_commit_provided)
fixing_commit_identified = "f8e7732ce69e5f3e591700bebbf00682ce7ab231"
print("\nAnalyses of repo: %s, commit: %s" % (remote_link, fixing_commit_provided))
git_analyse(local_link, fixing_commit_identified)

# Case 2
remote_link = "https://github.com/apache/pdfbox"
local_link = "../pdfbox"
if not os.path.isdir(local_link):
    Repo.clone_from(remote_link, local_link, progress=Progress())
fixing_commit = "4fa98533358c106522cd1bfe4cd9be2532af852"
print("\nAnalyses of repo: %s, commit: %s" % (remote_link, fixing_commit))
git_analyse(local_link, fixing_commit)


# Case 3
remote_link = "https://github.com/apache/tomcat80"
local_link = "../tomcat80"
if not os.path.isdir(local_link):
    Repo.clone_from(remote_link, local_link, progress=Progress())
fixing_commit = "ec10b8c785d1db91fe58946436f854dde04410fd"
print("\nAnalyses of repo: %s, commit: %s" % (remote_link, fixing_commit))
git_analyse(local_link, fixing_commit)