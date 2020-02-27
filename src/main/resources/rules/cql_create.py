# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from rules.helpers import deployed_helper
from com.xebialabs.deployit.plugin.api.deployment.planning import Checkpoint

helper = deployed_helper(deployed, steps)
checkpoints = delta.intermediateCheckpoints


def should_execute_script(fname):
    is_checkpointed = helper.extract_checkpointname(fname) in checkpoints
    return not checkpoints or is_checkpointed


all_script_files = [ff for ff in helper.list_create_scripts() if should_execute_script(ff)]
# Sort alphabetically
all_script_files.sort()

last_step = None
for script_file in all_script_files:
    last_step = helper.create_script_step(script_file)
    checkpoint = Checkpoint(delta._delegate, helper.extract_checkpointname(script_file), None)
    context.addStepWithCheckpoint(last_step, checkpoint)

# Add 'final' checkpoint once all steps are added.
if last_step:
    context.addCheckpoint(last_step, delta._delegate)
