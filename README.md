qurandownloader
=================================================

Python 3 script to download Quran MP3 Recitations
=================================================

This is a tiny utility to download MP3 quran recitations from web sites. I have included my
personal reciters (in the reciterList dict object), however the user is free to add his or her
own list from a file when executing the script.

1. In every request for download an MP3 file, the name of the reciter must be supplied with:
<pre>
-r Name or --reciter Name
</pre>
<code>Name</code> is anything you wish to call your reciter.

2. Multiple reciters can be requested:
<pre>
qurandownloader --reciter Name1 --reciter Name2 -r Name 3.
</pre>
If the MP3 recitations exist on the remote server exist, each recitation will be downloaded.

3. There are three ways to select a recitation:

[a]. --all or -a: This will download all 114 MP3 recitations or any that exist.
<pre>
Example: qurandownloader -r aKanakiri -r mAyyub -r mMinshawi --all (or -a)
 </pre>
[b]. --range or -g: This will download MP3 recitations with a specific range.
<pre>
Example: qurandownloader -r aAbdussamad --range 90-114
</pre>
All Suras from 90 all the way to Sura 114 for the reciter Abdulbassit Abdussamad will be downloaded.

[c]. --singleSura or -s: This will download a single Sura, or many Suras as you may specify.
<pre>
Example 1: qurandownloader -r aKanakiri -s10
Example 2: qurandownloader -r aMatrood -s7 -s11 -s 3 -s 8 -s 19 -s18
(spaces are irrelevant.)
</pre>
4. There are 2 ways to add your own list of reciters:

<b>First way: With a file</b>

This is done by supplying an -f argument to qurandownloader pointing to a file that contains a list of
reciters. To make your own list, you should MAKE SURE that the web server saves the MP3 recitations
in the common way most webservers do. That is: xxx.mp3, where xxx is any number from 1 - 114. If
you can access the MP3 file in such a way:
<pre>
http://some.host.com/somewhere/012.mp3
</pre>
then, you're ready. A file, then, should be prepared in the following format:

<pre>name_of_reciter:http://some.host.com/somewhere/</pre>
OR
<pre>name_of_reciter2 : http://another.host.net/some/remote/directory/</pre>
(see qurandownloader --help)

<b>Second way: by updating the script!</b>

At the end of the script where you can see:
<pre>
def main():
  try:
    d1 = QuranDownloader()
    reciter = str()
    dir1 = str()
</pre>
just make it look this way:
<pre>
def main():
  try:
    d1 = QuranDownloader()
<b>
    d1.reciterList.update({"yourReciter1":"http://some.remote.host.com/rest/of/url/"})
    d1.reciterList.update({"yourReciter2":"http://sremote.host.net/path/to/reciter/files/"})
</b> 
    reciter = str()
    dir1 = str()
</pre>
5. Directories: By default qurandownloader saves the files in a local directory, you can however
direct the script to save the downloaded files to another director:
<pre>
Example: qurandownloader -r aKhayat -d /home/Audios/ -s 15 -g 1-3
</pre>
6. There are two ways to download a random sura:
<pre>
[a]. qurandownloader -R
</pre>
This will download a random sura by a random reciter and exit.
<pre>
[b]. qurandownloader -r myReciter1 -R
</pre>
This will download a random sura by <i>myReciter</i>. You can specify as many reciters as you want, so
this is also valid:
<pre>
qurandownloader -r aKanakiri -r aMatrood -r aHuthayfi -R
</pre>
7. To list the available reciters, simply do: qurandownloader --list or -l

---
Abdalla S. Alothman

