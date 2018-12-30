import os
from core import execute
from core import utils

class GitScan(object):
	"""docstring for PortScan"""
	def __init__(self, options):
		utils.print_banner("Github Repo Scanning")
		utils.make_directory(options['env']['WORKSPACE'] + '/gitscan/')
		self.options = options
		self.initial()


	def initial(self):
		self.truffleHog()
		self.gitrob()

	def truffleHog(self):
		utils.print_good('Starting truffleHog')
		cmd = 'trufflehog --regex --entropy=True $TARGET | tee $WORKSPACE/gitscan/$TARGET-trufflehog.txt'
		cmd = utils.replace_argument(self.options, cmd)
		utils.print_info("Execute: {0} ".format(cmd))
		execute.run(cmd)
		utils.check_output(self.options, '$WORKSPACE/gitscan/$TARGET-trufflehog.txt')

	def gitrob(self):
		utils.print_good('Starting gitrob')
		really_target = utils.replace_argument(self.options, '$TARGET').split('/')[3] # only get organization name

		cmd = '$GO_PATH/gitrob -save $WORKSPACE/gitscan/$TARGET-gitrob -threads 10 -github-access-token $GITHUB_API_KEY {0}'.format(really_target)
		cmd = utils.replace_argument(self.options, cmd)
		utils.print_info("Execute: {0} ".format(cmd))
		execute.run(cmd)

	def gitscanner(self):
		pass
		# cmd = '$PLUGINS_PATH/reposcanner.py -r https://github.com/Dionach/reposcanner -v -a -c 30'