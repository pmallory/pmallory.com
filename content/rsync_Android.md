title: rsync and Android
date: 2016-10-1
category: tech

Here's what you need to transfer files to an Android phone over the network using rsync.

sshd for Android: [SSHelper](http://arachnoid.com/android/SSHelper/)

How to use rsync on a nonstandard port:

    :::bash
    rsync -rv -e "ssh -p 2222" ~/Music 192.168.0.100:/sdcard/Music

I'm not using the compression flag (-z) because my music library consists of files that are already compressed.
Even if they weren't I'm not sure if compression would even be a time saver considering my phone's pitiful CPU and that this transfer is over the speedy local network.

The `-e "ssh -p 2222"` bit is how you get rsync to connect to sshd on a nonstandard port, SSHelper would need to run as root to get ssh on port 22.

[SSHelper](http://arachnoid.com/android/SSHelper/) is an open source app that supports several other Unixy file transfer protocols in addition to ssh.
They author is pretty cool too, browse his page for all kinds of interesting things.

The syncing process is pretty slow, but it works.
iPods also just worked but the world seems to have moved on from people owning their own digital music libraries.
Oh well.

