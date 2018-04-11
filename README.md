# Helpful Scripts
An arrary of helpful scripts created/found 

## Copying file to remote server using proxy server
This Bash will copy a file locally and move it to a remote server passing through a proxy server with passwordless SSH.

          ssh user@server1 "ssh user@server2 \"cd /home/dir/scripts && sudo cat > remoteFile.py\"" < ./localFile.py
