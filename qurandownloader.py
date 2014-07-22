#!/usr/bin/python3

import sys, re, urllib.request, argparse, os, random
class QuranDownloader(object):
  def __init__(self):
    self.reciterList = {"aJabir" : "http://ia601604.us.archive.org/1/items/Ali__Jaber/",
                        "aHuthayfi": "http://download.quran.islamway.net/quran3/183/",
                        "aMatrood": "http://ia700405.us.archive.org/2/items/TvQuran.com__Al-Mattrod/",
                        "khQahtani": "http://ia801508.us.archive.org/5/items/Khaled_Al-Qahtani/",
                        "hSnan": "http://ia600208.us.archive.org/11/items/Hamad_Sinan/",
                        "mMinshawi": "http://ia600508.us.archive.org/15/items/Mohamed_Seddik_Al-Menshawi/",
                        "aKhayat": "http://ia600309.us.archive.org/0/items/Abdullah_Khayat/",
                        "mAyyub": "http://ia700301.us.archive.org/15/items/Mohamed_Ayoub/",
                        "aAbdussamad": "http://ia700309.us.archive.org/6/items/Abdul_Basset_Abdul_Samad_Mujawwad/",
                        "aKanakiri" : "http://ia600305.us.archive.org/7/items/Abdul_Hadi_Kanakeri/"}
    self.description = "Download Quran recitations by reciter, range, or single sura."
    self.version = "%(prog)s 1.8. Copyright © Abdalla S. Alothman Kuwait 2014"
    self.name = "qurandownloader"
    self.sdir=str()
    self.lastFile = str()

  def setDir(self, saveDir):
    #print(os.access(saveDir, os.R_OK))
    if not os.path.exists(saveDir):
      os.makedirs(saveDir)
    self.sdir = saveDir

  def cleanInterruptedDownload(self):
    print("Cleaning up...")
    if os.path.exists(self.lastFile):
      print("Deleting incomplete file: {}".format(self.lastFile))
      os.remove(self.lastFile)

  def availableReciters(self):
    print("Available Reciters:")
    for l, r, in enumerate(self.reciterList.keys(), 1):
      print("{}: {}".format(l, r))
  
  def checkAvailability(self, reciter):
    if reciter not in self.reciterList:
      print("Error: {} is not in the list.".format(reciter))
      print("Please use select a reciter from the available list.")
      self.availableReciters()
      return False
    else:
      return True
  
  def updateList(self, listFile):
    try:
      with open(listFile, "r") as lFile:
        for lines in lFile:
          lines.strip()
          r1 = re.search(r"^([a-zA-Z]{1,20})\s{0,5}[:,\.-]\s{0,5}(http://.{5,150}/)$", lines)
          if not r1:
            print("{} is improperly formatted.".format(lines.strip()))
            print("""Acceptable format is: nameOfReciter : http://somesite.com/"
            Examples: myReciter:http://
                      myReciter,http://site.com/
            the separator bteween the name and the URL can be any of: \":,.-\" with or without spaces.
            The URL must start with http:// and must end with a \'/\'""")
            print("Skipping...")
          elif r1:
            self.reciterList.update(dict({r1.group(1): r1.group(2)}))
            print("Successfully added reciter:{} with URL:{}".format(r1.group(1), r1.group(2)))
    except IOError as e:
      print("Problem opening file: {}".format(listFile))
      print(e)
      raise SystemExit()
      

  def rangeValidator(self, sRange):
    m1 = re.search(r"^\s{0,5}(\d{1,3})\s{0,5}(?:-|:|,)\s{0,5}(\d{1,3})",sRange)
    result = list()
    if m1:
      fromSura = int(m1.group(1))
      toSura = int(m1.group(2))
      if fromSura > toSura:
        print("illegal values.")
        vTemp = fromSura
        fromSura = toSura
        toSura = vTemp
        print("corrected range from {} to {}-{}".format(sRange, fromSura, toSura, sep=""))
      elif fromSura > 114 or toSura > 114:
        print("Out of range. Maximum is: 114. {} {}".format(fromSura, toSura))
        return
      elif fromSura == toSura:
        print("Inapplicable range. Please use --singlesura instead.")
        return
      elif fromSura <= 0 or toSura <= 0:
        print("Range is too small. Acceptable range starts from 1 to 114.")
        return
      print("Sucessful match found.")
      result.append(fromSura)
      result.append(toSura)
      return result
    else:
      print("{} is not an acceptable range format.".format(sRange))
      sys.exit()
  
  def randSelector(self):
    step = random.randrange(1, 53)
    l = list(self.reciterList.keys())
    random.shuffle(l)
    reciter = random.choice(l)
    sura = random.randrange(1, 115, step)
    return(reciter, int(sura))

  def downloadMulti(self, reciter, fromSura=1, toSura=114):
    for fp in list(range(fromSura, toSura + 1)):
      fName = reciter + "-" + str(fp).zfill(3) + ".mp3"
      url = "{}{}.mp3".format(self.reciterList[reciter], str(fp).zfill(3))
      print("Downloading {}\nFrom: {}".format(fName, url))
      self.downloadURL(fName, url)
      
  def downloadSingle(self, reciter, suraNumber):
    if suraNumber > 114 or suraNumber <= 0:
      print("Error processing {}.\nSura number should be between 1 to 114".format(suraNumber))
      return
    fName = reciter + "-" + str(suraNumber).zfill(3) + ".mp3"
    url = "{}{}.mp3".format(self.reciterList[reciter], str(suraNumber).zfill(3))
    print("Downloading {}\nFrom: {}".format(fName, url))
    self.downloadURL(fName, url)

  def downloadURL(self, fileName, qurl):
    rq = urllib.request.urlopen(qurl)
    if not rq.info()['Content-Type'].startswith("audio/"):
      print("Non-Audio File. Please check that the URL:\n{}\npoints to a valid audio file.\nExiting...".format(qurl))
      sys.exit()
    fSize = int(rq.info()['Content-Length'])
    print("File szie: {} bytes.".format(fSize))
    qf = os.path.join(self.sdir, fileName)
    downloadedChunk = 0
    blockSize = 2048 # (1024 * 2 - OK) (1024 * 8 = 8192)

    with open(qf, "wb") as sura:
      while True:
        chunk = rq.read(blockSize)
        if not chunk:
          print("Download Complete. Stored as {}.".format(qf, fSize))
          break
        downloadedChunk += len(chunk)
        self.lastFile = qf
        sura.write(chunk)
        progress = float(downloadedChunk) / fSize
        stat = r" Saving:ls {0} [{1:.2%}] of {2} bytes.".format(downloadedChunk, progress, fSize)
        stat = stat + chr(8) * (len(stat) + 1)
        sys.stdout.write(stat)
        sys.stdout.flush()

def main():
  try:
    d1 = QuranDownloader()
    reciter = str()
    dir1 = str()

    ap = argparse.ArgumentParser(description=d1.description, prog=d1.name)
    ap.add_argument("-l", "--list", action="store_true", default=False, dest="listReciters",
                    help="List available reciters.")
    ap.add_argument("-R", "--random", action="store_true", dest="rand11", help="Download random sura by a random reciter by using: qurandownloader.py -R. If you specify a reciter or more with -r, a random sura by that reciter would be downloaded. Example: qurandownloader -r aMatrood -R")
    ap.add_argument("-v", "--version", action="version", version=d1.version)
    ap.add_argument("-f", "--reciterlist", type=str, dest="rFile",
                    help="Read a list of reciters from a file. The list must be properly formatted.\nEach line beings with a name of a reciter: myReciter, followed by either a ':' or a ',' or a '-' or even a '.' followed by the URL. The URL must be terminated with a '/'. Example Entry: myReciter:http://www.somesite/remoteDir/") 
    ap.add_argument("-d", "--dir", type=str, dest="directory",
                    help="Save downloaded files to a specific directory.")
    ap.add_argument("-r", "--reciter", type=str, action="append", dest="rList",
                    help="The reciter(s) to target. Use --list to see the available list.")
    ap.add_argument("-s", "--singlesura", type=str, action="append", dest="sList",
                    help="Download a single sura or a list of suras: -s 1 -s 10 -s 93")
    ap.add_argument("-a", "--all", action="store_true", dest="dMulti", default=False,
                    help="Download all Quran files")
    ap.add_argument("-g", "--range", type=str, action="append", dest="rrange",
                     help="Fetch a list of suras from a range. Examples: -g1-10, -g 5:9, --range 40,90")

    ar = ap.parse_args()
    
    if ar.rand11:
      if not ar.rList:
        result = d1.randSelector()
        d1.downloadSingle(result[0], result[1])
      else:
        for r in ar.rList:
          result = d1.randSelector()
          d1.downloadSingle(r, result[1])
      sys.exit()
    
    if ar.rFile:
      d1.updateList(ar.rFile)
    
    if ar.directory:
      dir1=ar.directory
      d1.setDir(ar.directory)

    if ar.listReciters:
      d1.availableReciters()
      sys.exit()

    if not ar.rList:
      print("{}: {}".format(ap.prog, ap.description))
      print("[Error]: Must supply at least one reciter. Please use --list.")
      sys.exit()

    for r in ar.rList:
      if d1.checkAvailability(r):
        if ar.dMulti:
          d1.downloadMulti(r)
          ar.dMulti = False
        if ar.sList:
          for sura in ar.sList:
            d1.downloadSingle(r, int(sura))
          #del ar.sList[:]
        if ar.rrange:
          for i in ar.rrange:
            rng = d1.rangeValidator(i)
            d1.downloadMulti(r, rng[0], rng[1])
            #ar.rrange.remove(i)
        continue
  except KeyboardInterrupt:
    print("Terminating download.")
    d1.cleanInterruptedDownload()
    sys.exit(0)

main()

