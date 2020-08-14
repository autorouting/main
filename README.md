<!-- Temporary, for developers -->
# Best Practices (READ FIRST BEFORE CHANGING ANYTHING)
1. Always use your own branch to write and test code. To keep your branch up-to-date with master, merge your branch with master (<code>git merge master</code>). To add to master, pull request from your own branch. Be sure to merge first.
2. Don't push broken code.
3. Try to commit single files (every time you update something). Commit often.

# Usage
Edit the addresses in <code>locations.txt</code>. Have the address for the depot be the first line and the address for the second stop be the second line. Make sure there are no empty lines. Then, run <code>genmapslink.py</code> and follow the output Google Maps link.

# Dependencies
* \_\_future__
* geopy
* networkx
* osmnx (It seems that this package is currently broken on pip)
* ortools
* conda (Used to install osmnx)

## Installing Dependencies
Install conda and add it to your PATH. On Windows, run <code>InstallDependencies.bat</code>. On MacOS, run <code>install_libraries.command</code>. On Linux, run <code>InstallDependencies.sh</code>.
