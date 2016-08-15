# Links
**Links is a (Relatively) Powerfull tool to extract Links and Resources from Web Pages**

**NOTE** Returned links will be unique and will not repeat.

### Installation

    $ sudo su
    # pip install -r requirements.txt
    # chmod +x ./links.py

You can also make a `ln -s` in your `/usr/bin` folder

### Usage

```
usage: links [-h] [-l] [-d] [-a] [-r] [-e E] url

positional arguments:
  url         target web page

optional arguments:
  -h, --help  show this help message and exit
  -l          output found links as plain list
  -d          download resource directly in CWD
  -a          select resource and visible links
  -r          select only resource links (audio,video,img,background)
  -e E        select links that follow RegEx
  -m M        select RegEx for substitution match
  -s S        select string to substitute
```

#### Classic
Get Visible (a href) links from `google.com` Homepage

    links.py https://google.com

#### Media Support
Get Resource (img,video,audio,etc..) links from `google.com` Homepage

    links.py -r https://google.com

Get Resource and Visible links from `google.com` Homepage

    links.py -a https://google.com

#### Media download (wget or direct)
Download Resource (img,video,audio,etc..) from `google.com` Homepage

    links.py -rl https://google.com | wget -i -

Or

    links.py -rd https://google.com

#### RegEx Support
Get Visible links that contains `google` from `google.com`

    links.py -e "(.*google.*)" https://google.com

Get Visible links that use `https` from `google.com`

    links.py -e "(https://.*)" https://google.com

Get `.png` or `.jpg` Resource from `google.com`

    links.py -re "(.*\.jpg|.*\.png)" https://google.com

#### RegEx Substitution Support
Strip all `https` links to `http`

    links.py -m "https" -s "http" https://google.com
