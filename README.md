                      _                 
                     | |                
 _ __   __ _ _ __ ___| |__   __ _ _ __  
| '_ \ / _` | '__/ __| '_ \ / _` | '_ \ 
| |_) | (_| | | | (__| | | | (_| | | | |
| .__/ \__,_|_|  \___|_| |_|\__,_|_| |_|
| |                                     
|_|  

parchan is Python-based script for making a thread dumps from https://2ch.hk imageboard

Requirements: 
    Python 3 (https://www.python.org/)
    Requests lib (https://pypi.org/project/requests/)

Syntax:
    parchan <thread_url> [flags]
    
Flags: 
    --help                      - shows this message, exit script
    --no-files                  - saving thread without attachments 
    --path <path>               - saving thread to custom path, default is ../ 
    --proxy <proxy_url>         - connecting to board via custom proxy, default is none 
    --default-proxy <proxy_url> - setting default proxy to <proxy_url>, exit script
    --default_path <path>       - setting default saving thread path to <path>, exit script