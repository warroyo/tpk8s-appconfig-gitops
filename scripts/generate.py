from pathlib import Path
import logging
import yaml
import subprocess
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parent = Path(__file__).resolve().parents[1]
configs = str(parent.joinpath("configs"))
ytt = str(parent.joinpath("ytt"))
pathlist = parent.rglob('ini_config.yml')
for path in pathlist:
    path_in_str = str(path)
    app_dir = path.parent
    logging.info(f"generating ini config for {path_in_str}")
    with open(path_in_str, 'r') as file:
        config = yaml.safe_load(file)
    
    env = config['env']
    customer = config['customer']

    try:
        result = subprocess.check_output(["ytt", f"--data-values-file={configs}/base/global.yaml", f"--data-values-file={configs}/envs/{env}.yaml", f"--data-values-file={configs}/customers/{customer}.yaml", "-f", f"{ytt}/ini-generate.yaml"], text=True)
        logging.info(f"writing ini secret file to {app_dir}")
        file=f"{app_dir}/ini-sectret.yml" 
        with open(file, 'w') as filetowrite:
            filetowrite.write(result)

    except subprocess.CalledProcessError as e:
        logging.fatal(e.output)
        sys.exit(1)
