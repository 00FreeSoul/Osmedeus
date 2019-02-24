import os, socket, time
from core import utils
from pprint import pprint
from configparser import ConfigParser, ExtendedInterpolation

# Console colors
W = '\033[1;0m'   # white
R = '\033[1;31m'  # red
G = '\033[1;32m'  # green
O = '\033[1;33m'  # orange
B = '\033[1;34m'  # blue
Y = '\033[1;93m'  # yellow
P = '\033[1;35m'  # purple
C = '\033[1;36m'  # cyan
GR = '\033[1;37m'  # gray

__author__ = '@j3ssiejjj'
__version__ = '1.0'

def banner():
    print(r"""{1}

                       `@@`
                      @@@@@@
                    .@@`  `@@.
                    :@      @:
                    :@  {5}:@{1}  @:                       
                    :@  {5}:@{1}  @:                       
                    :@      @:                             
                    `@@.  .@@`
                      @@@@@@
                        @@
                     {0}@{1}  {1}@@  {0}@{1}               
                    {0}+@@{1} {1}@@ {0}@@+{1}                    
                 {5}@@:@#@,{1}{1}@@,{5}@#@:@@{1}           
                ;@+@@`#@@@@#`@@+@;
                @+ #@@@@@@@@@@# +@
               @@  @+`@@@@@@`+@  @@
               @.  @   ;@@;   @  .@
              {0}#@{1}  {0}'@{1}          {0}@;{1}  {0}@#{1}

                     
             Osmedeus v{5}{6}{1} by {2}{7}{1}

                    ¯\_(ツ)_/¯
        """.format(C, G, P, R, B, GR, __version__, __author__))

def parsing_config(config_path, args):
    options = {}
    #config to logging some output
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(config_path)

    ##some default path
    go_path = str(os.getenv("GOPATH"))
    github_api_key = str(os.getenv("GITROB_ACCESS_TOKEN"))
    cwd = str(os.getcwd())

    config.set('Enviroments', 'cwd', cwd)
    config.set('Enviroments', 'go_path', go_path)
    config.set('Enviroments', 'github_api_key', github_api_key)
    workspace = cwd + "/workspace/"

    ##config of the tool
    if args.slow:
        speed = "slow"
    else:
        speed = "quick"

    module = str(args.module)
    debug = str(args.debug)

    config.set('Mode', 'speed', speed)
    config.set('Mode', 'module', module)
    config.set('Mode', 'debug', debug)

    ##target stuff
    #parsing agument


    git_target = args.git if args.git else None
    burpstate_target = args.burp if args.burp else None
    target_list = args.targetlist if args.targetlist else None
    company = args.company if args.company else None



    if args.target:
        target = args.target
        output = args.output if args.output else args.target
        company = args.company if args.company else args.target

        strip_target = target.replace('https://', '').replace('http://', '')
        if '/' in strip_target:
            strip_target = strip_target.split('/')[0]

        if args.workspace:
            if args.workspace[-1] == '/':
                workspace = args.workspace + options['env']['STRIP_TARGET']
            else:
                workspace = args.workspace + '/' + options['env']['STRIP_TARGET']
        else:
            workspace += strip_target

        ip = socket.gethostbyname(strip_target)




    # workspace += '/' + strip_target

    config.set('Target', 'git_target', str(git_target))
    config.set('Target', 'burpstate_target', str(burpstate_target))
    config.set('Target', 'target_list', str(target_list))
    config.set('Target', 'output', str(output))
    config.set('Target', 'target', str(target))
    config.set('Target', 'strip_target', str(strip_target))
    config.set('Target', 'company', str(company))
    config.set('Target', 'ip', str(ip))
    config.set('Enviroments', 'workspace', str(workspace))


        #create workspace folder for the target
    utils.make_directory(workspace)

        # options['env']['COMPANY'] = args.target
        #checking for connection to target




    #save the config
    with open(config_path, 'w') as configfile:
        config.write(configfile)


    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(config_path)
    sections = config.sections()

    for sec in sections:
        for key in config[sec]:
            # if key = 
            options[key.upper()] = config.get(sec, key)
            # print("{0}:{1} -> ".format(sec, key) ,config.get(sec, key))
        # print('-'*20)

    # print(config.get('Enviroments', 'CWD'))
    # print(config.get('Enviroments', 'WORKSPACE'))
    # print(config.get('Enviroments', 'PLUGINS_PATH'))
    # print(config.get('Enviroments', 'GO_PATH'))
    # print('-'*20)
    # print(config.get('Resources', 'directory_full'))
    # print(config.get('Resources', 'domain_full'))


    #make all the keys upper and return the options

    return options



# if __name__ == "__main__":
# 	parsing_config("/Users/j3ssie/myGit/Osmedeus/config.conf")
