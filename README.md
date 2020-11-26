# Usage on a local device with Python
Install dependencies (as listed below). Run <code>run_gui_single.bat</code> (Windows) or <code>run_gui_single.command</code> (Mac) or <code>run_gui_single.sh</code> (Linux).

# How to set up an Autorouting web app for your area
Create an Apache web server on a Linux machine and enable Python CGI. Use OSMNX and Pickle to replace the current <code>graph</code> file for that of your area. Add <code>email_config.txt</code>, <code>genmapslink_web.py</code>, <code>graph</code>, <code>onevehicleroutegen_web.py</code>, <code>send_email.py</code>, and <code>webgui.py</code> to the cgi-bin. Add <code>index.html</code> and <code>style.css</code> to the HTML folder. Create instruction files (routing.mp4 and usageguide.pdf) and add them to the HTML folder. In <code>webgui.py</code>, add your API key and change the Python interpreter (be sure to install dependencies as listed below). Change the contents of <code>email_config.py</code>. In <code>webgui.py</code>, change <code>/var/www/html/delivery/style.css</code> to <code>/var/www/html/style.css</code>.

# Dependencies
* \_\_future__
* geopy
* googlemaps
* networkx
* osmnx
* ortools
