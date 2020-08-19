<!-- Temporary, for developers -->
<!--# Best Practices (READ FIRST BEFORE CHANGING ANYTHING)
1. Always use your own branch to write and test code. To keep your branch up-to-date with master, merge your branch with master (<code>git merge master</code>). To add to master, pull request from your own branch. Be sure to merge first.
2. Don't push broken code.
3. Try to commit single files (every time you update something). Commit often.
-->
# Usage
Enter each address into a seperate line of <code>addresses.txt</code>, then run <code>gen_input.py</code>. For each address, a Google Maps link will be opened. Wait for each Google Maps URL to redirect and change from a short URL to a really long URL. For every URL, copy the entire final URL, from the <code>https://</code> to the end of the link, and paste into <code>locations.txt</code>. Have the link for the driver's home be the first line and the link for the restraunt be the second line. Make sure there are no empty lines. Then, open <code>launchprogram.command</code> and follow the output Google Maps link.

# Dependencies
* \_\_future__
* geopy
* networkx
* osmnx (It seems that this package is currently broken on pip)
* ortools
* conda (Used to install osmnx)

<h2>Installing Dependencies</h2>
Install conda and add it to your PATH. On Windows, run <code>InstallDependencies.bat</code>. On MacOS, run <code>install_libraries.command</code>. On Linux, run <code>InstallDependencies.sh</code>.
