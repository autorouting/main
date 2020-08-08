# Best Practices (READ FIRST BEFORE CHANGING ANYTHING)
1. Always use your own branch to write and test code. Use pull requests to merge working code with master. To keep your branch up-to-date with master, merge your branch with master (<code>git merge master</code>)
2. Don't push broken code.

# Usage
Edit the addresses in <code>locations.txt</code>. Make sure there are no empty lines. Then, run <code>genmapslink.py</code> and follow the output Google Maps link.

# Dependencies
* \_\_future__
* geopy
* networkx
* osmnx (It seems that this package is currently broken on pip)
* ortools
* conda (Used to install osmnx)

## Installing Dependencies
Install conda and add it to your PATH. On Windows, run <code>InstallDependencies.bat</code>. On MacOS, run <code>install_libraries.command</code>. On Linux, run <code>InstallDependencies.sh</code>.
