import extract_module as em
import download_module as dm
dm.download_tar("http://www.shallalist.de/Downloads/shallalist.tar.gz","1.tar")
dm.download_tar("http://dsi.ut-capitole.fr/blacklists/download/blacklists.tar.gz","2.tar")
dm.download_tar("http://squidguard.mesd.k12.or.us/blacklists.tgz","3.tar")
em.extract_tar("1.tar")
em.extract_tar("2.tar")
em.extract_tar("3.tar")



