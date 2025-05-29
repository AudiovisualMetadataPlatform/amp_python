#!/bin/env python3

from amp.package import *
from amp.prereq import pick_program
import argparse
import logging
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil

def main():
    parser = argparse.ArgumentParser()    
    parser.add_argument("--debug", default=False, action="store_true", help="Turn on debugging")    
    parser.add_argument("--package", default=False, action="store_true", help="Build package instead of install")
    parser.add_argument("destination", help="Destination for build (should be an AMP_ROOT for non-package)")
    args = parser.parse_args()
    logging.basicConfig(format="%(asctime)s [%(levelname)-8s] (%(filename)s:%(lineno)d)  %(message)s",
                        level=logging.DEBUG if args.debug else logging.INFO)


    sif = Path(sys.path[0], 'amp_python.sif')
    recipe = Path(sys.path[0], 'amp_python.recipe')

    # Build the container
    if not sif.exists() or recipe.stat().st_mtime > sif.stat().st_mtime:
        # build it
        logging.info(f"Building {sif!s}")        
        p = subprocess.run(['apptainer', 'build', '--force', '--fakeroot', str(sif), str(recipe)])
        if p.returncode != 0:
            logging.error(f"Building container has failed with return code {p.returncode}")
            exit(1)
    else:
        logging.info(f"{sif!s} is up to date")

    # Install the container
    destdir = Path(args.destination)
    if args.package:
        # create a temporary directory for the build.
        tempdir = tempfile.TemporaryDirectory()
        destdir = Path(tempdir.name)

    (destdir / "amp_python").mkdir(parents=True, exist_ok=True)
    destsif = destdir / "amp_python" / sif.name
    logging.info(f"Copying {sif!s} to {destsif!s}")
    try: 
        shutil.copyfile(sif, destsif)
        # copyfile doesn't copy permissions bits, so get them too...
        shutil.copystat(sif, destsif)
    except Exception as e:
        logging.error(f"Failed to copy sif file: {e}")
        exit(1)

    # Package it, if needed
    if args.package:
        try:
            new_package = create_package('amp_python', '2.0.0', 'amp_python',
                                         Path(args.destination), destdir / "amp_python",                                         
                                         hooks={'post': 'postinstall.py'},
                                         arch_specific=True)
            logging.info(f"New package in {new_package}")    
        except Exception as e:
            logging.error(f"Failed to build backage: {e}")
            exit(1)


if __name__ == "__main__":
    main()
