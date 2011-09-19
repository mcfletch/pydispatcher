#! /bin/bash

rsync -avP -e ssh docs/* mcfletch,pydispatcher@web.sourceforge.net:htdocs/
