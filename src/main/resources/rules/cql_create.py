import rules.helpers
reload(rules.helpers)
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
