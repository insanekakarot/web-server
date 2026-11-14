# Web Server
  
  An OpenSource Web Server by [@insanekakarot](https://github.com/insanekakarot) & [@syedovaisuallah](https://github.com/SYEDOVAISULLAH)

  Install TailScale using command in linux;
  ``` bash
    `sudo apt update`
    `curl -fsSL https://tailscale.com/install.sh | sh`
  ```
  or Visit [TailScale](https://tailscale.com/docs/install/linux) for complete installation guide.

  After installing check TailScale Downloaded using version verification;
    
    ``` bash
    `tailscale --version`
    ```

## Running Server
  Run `server.py` & tailscale funnel using `sudo tailscale funnel --tls-terminated-tcp=10000 tcp://127.0.0.1:1101`
  It will make a tcp connection for public access.
  The response will something in this format:
  ``` bash
  Available on the internet:

    |-- tcp://<hostname>.<node>.ts.net:10000 (TLS terminated)
    |-- tcp://<xx.xxx.xxx.xx:10000> # TailScale Generated IP
    |-- tcp://[xx7x:xxxc:x1ex::xxxx:5xxx]:10000
    |--> tcp://127.0.0.1:1101`
  ```
  
  Use `sender.py` and it's HOST variable value into `<hostname>.<node>.ts.net` and use the same port (Recommended)

  Now send message from `sender.py` file, when message input bar visible & check the log in terminal where `server.py` executes.

 


