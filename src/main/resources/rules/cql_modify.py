# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from rules.helpers import deployed_helper
from com.xebialabs.deployit.plugin.api.deployment.planning import Checkpoint
from sets import Set
import filecmp
from com.xebialabs.deployit.plugin.api.deployment.specification import Operation

helper = deployed_helper(deployed, steps)
previous_helper = deployed_helper(previousDeployed, steps)

checkpoints = delta.intermediateCheckpoints


def should_execute_script(fname, h):
    is_checkpointed = h.extract_checkpointname(fname) in checkpoints
    return not checkpoints or is_checkpointed


def difference(left_set, right_set, check_contents, left_helper, right_helper):
    s = Set()
    for f in left_set:
        if not should_execute_script(f, left_helper):
            pass
        elif f not in right_set:
            s.add(f)
        elif check_contents and not filecmp.cmp(left_helper.path_of(f), right_helper.path_of(f), shallow=False):
            s.add(f)
        else:
            pass
    return s


current_files = helper.list_create_scripts()
previous_files = previous_helper.list_create_scripts()
current_set = Set(current_files)
previous_set = Set(previous_files)

check_contents = previous_helper.deployed.executeModifiedScripts and previous_helper.deployed.executeRollbackForModifiedScripts
missing_scripts = list(difference(previous_set, current_set, check_contents, previous_helper, helper))
# Reverse sort, as we're going to roll these back.
missing_scripts.sort(reverse=True)

last_step = None
for missing_script in missing_scripts:
    rollback_script = previous_helper.rollback_script_for(missing_script)
    if rollback_script:
        last_step = previous_helper.destroy_script_step(rollback_script, previous_helper.deployed.modifyOptions)
        checkpoint = Checkpoint(delta._delegate, helper.extract_checkpointname(missing_script), Operation.DESTROY)
        context.addStepWithCheckpoint(last_step, checkpoint)

check_contents = helper.deployed.executeModifiedScripts
new_scripts = list(difference(current_set, previous_set, check_contents, helper, previous_helper))
# Sort in ascending order.
new_scripts.sort()

for new_script in new_scripts:
    last_step = helper.create_script_step(new_script, helper.deployed.modifyOptions)
    checkpoint = Checkpoint(delta._delegate, helper.extract_checkpointname(new_script), Operation.CREATE)
    context.addStepWithCheckpoint(last_step, checkpoint)

if last_step:
    context.addCheckpoint(last_step, delta._delegate)
