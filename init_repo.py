"""Automate Project Creation
Usage:
    init_repo.py <project_name> <token> <base_dir> (--readme | --load_readme=<path>)

Options:
    -h --help                  Shows this screen.
    -r --readme                Create a README file.
    -lr --load_readme=<path>   Path to an existing README file to include in the project  [default: None].
"""

import sys
import os
import shutil
import subprocess
from github import Github
from docopt import docopt


class CreateOrLoadReadme(Exception):
	def __init__(self, expr, msg):
		self.expr = expr
		self.msg = msg


def create_project(name, token, base_dir, readme, load_readme):
    try:
        g = Github(token)
        user = g.get_user()
        repo = user.create_repo(name)
    except:
        print('Not a valid token')
        sys.exit()

    
    project_path = '/'.join([base_dir, name])

    try:
        os.mkdir(project_path)
    except FileExistsError:
        print('Directory already exists')
        sys.exit()

    if readme:
        with open('/'.join([project_path, 'README.md']), 'w') as file_obj:
            file_obj.write(': '.join(['New project created', name]))

    elif load_readme:
    	try:
    		shutil.copy(load_readme, project_path)
    	except:
    		print(' '.join(['Unable to copy',load_readme, 'check if path exists']))
        

    subprocess.call(['sh', './automate_git.sh', name, user.login])



if __name__ == '__main__':
    args = docopt(__doc__)

    if args['--readme'] and args['--load_readme'] != 'None' or \
         not args['--readme'] and args['--load_readme'] == 'None':
        raise CreateOrLoadReadme([args['--readme'], args['--load_readme']], 'You can either load or create new readme.')

    create_project(args['<project_name>'], args['<token>'], args['<base_dir>'],
                    args['--readme'], args['--load_readme'])


