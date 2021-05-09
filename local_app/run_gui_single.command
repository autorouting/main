cd "$(dirname "$BASH_SOURCE")";
source activate ox;
echo Launching Routing GUI ...
python gui.py
echo done
exit;