from distutils.core import setup
import glob

# Assume everything in the script directory is an executable
scriptlist = glob.glob('Scripts/*.py') + ['Scripts/py']

setup(name="Pistol",
      version="0.2",
      description="Pistol: Python Scientific Toolkit",
      long_description="Pistol: Python Scientific Toolkit",
      author="Rick Muller",
      author_email="rpm@wag.caltech.edu",
      url=None,
      license="GPL",
      packages=['Pistol','Pistol/DVR'],
      scripts=scriptlist)

      
      
      
