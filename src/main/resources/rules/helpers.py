# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re
from os.path import exists, join, isfile
from os import listdir
import org.slf4j.LoggerFactory as LoggerFactory


class deployed_helper:
    def __init__(self, deployed, steps):
        self.logger = LoggerFactory.getLogger("cassandra")
        self.deployed = deployed
        self.__deployed = deployed._delegate
        self.script_pattern = re.compile(self.deployed.scriptRecognitionRegex)
        self.rollback_pattern = re.compile(self.deployed.rollbackScriptRecognitionRegex)
        self.artifact_folder = deployed.getFile().path
        self.steps = steps
        self.logger.info("deployed_helper Init done")

    def __list_scripts(self, func):
        return [ff for ff in listdir(self.artifact_folder) if isfile(self.path_of(ff)) and func(ff)]

    def list_create_scripts(self):
        return self.__list_scripts(self.is_create_script)

    def list_rollback_scripts(self):
        return self.__list_scripts(self.is_rollback_script)

    def rollback_script_for(self, script_name):
        if self.is_create_script(script_name):
            rollback_script = self.script_pattern.match(script_name).group(1) + self.deployed.rollbackScriptPostfix
            return rollback_script if exists(self.path_of(rollback_script)) else None
        else:
            raise Exception("Expected a create script, got " + script_name)

    def path_of(self, script_name):
        return join(self.artifact_folder, script_name)

    def is_script(self, script_name):
        return self.is_create_script(script_name) or self.is_rollback_script(script_name)

    def is_create_script(self, script_name):
        return True if self.script_pattern.match(script_name) else False

    def is_rollback_script(self, script_name):
        return True if self.rollback_pattern.match(script_name) else False

    def extract_checkpointname(self, script_name):
        match = self.script_pattern.match(script_name)
        if not match:
            rollback_match = self.rollback_pattern.match(script_name)
            postfix = self.deployed.rollbackScriptPostfix
            rm = rollback_match.group(0) if rollback_match else None
            print rm
            rm = rm[:-len(postfix)] if rm and rm.endswith(postfix) else None
            print rm
            return rm
        else:
            return match.group(1) if match else None

    def create_script_step(self, script, options=None):
        self.logger.info("Create step for %s" % script)
        step = self.__script_step(script, self.deployed.createOrder, "Run")
        return step

    def destroy_script_step(self, script, options=None):
        step = self.__script_step(script, self.deployed.destroyOrder, "Rollback")
        return step

    def __script_step(self, script, order, verb):
        self.logger.info("in script step")
        step = self.steps.os_script(
            description="%s %s on %s" % (verb, script, self.deployed.container.name),
            order=order,
            script=self.deployed.getExecutorScript(),
            target_host=self.deployed.container.host,
            freemarker_context={'cqlScriptToExecute': script, 'deployed': self.__deployed,
                                'container': self.deployed.container}
        )

        return step
