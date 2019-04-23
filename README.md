\########     ###    ########   ######  ##     ##    ###    ##    ## <br/>
\##     ##   ## ##   ##     ## ##    ## ##     ##   ## ##   ###   ## <br/>
\##     ##  ##   ##  ##     ## ##       ##     ##  ##   ##  ####  ## <br/>
\########  ##     ## ########  ##       ######### ##     ## ## ## ## <br/>
\##        ######### ##   ##   ##       ##     ## ######### ##  #### <br/>
\##        ##     ## ##    ##  ##    ## ##     ## ##     ## ##   ### <br/>
\##        ##     ## ##     ##  ######  ##     ## ##     ## ##    ## <br/>

**parchan** is Python-based script for making a thread dumps from [2ch.hk](https://2ch.hk) imageboard

**Requirements:**
    [Python 3](https://www.python.org/)
    [Requests lib](https://pypi.org/project/requests/)

**Syntax:**
    parchan \<thread_url\> \[flags\]
    
**Flags:**
    --help                      - shows this message, exit script
    --no-files                  - saving thread without attachments 
    --path <path>               - saving thread to custom path, default is ../ 
    --proxy <proxy_url>         - connecting to board via custom proxy, default is none 
    --default-proxy <proxy_url> - setting default proxy to <proxy_url>, exit script
    --default_path <path>       - setting default saving thread path to <path>, exit script
