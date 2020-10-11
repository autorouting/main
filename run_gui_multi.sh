cd "$(dirname "$BASH_SOURCE")";
source activate ox;
echo Launching Routing GUI ...
python gui_multi.py
echo done
exit;