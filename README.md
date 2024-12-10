# Generating layered Configs for TPK8s gitops

This repo is an example of how to use an automated process to generated configs based on different layers. In this case the layers are base defaults, then environment specific data, then customer specific data related to the specific app deploy. This could be extended to include more layers or fewer. This example generates `ini` files in a k8s secret that can then be synced into a space using gitops.


## How it works

1. configs are place in the `configs` directory using a specific folder structure. these configs are yaml, this is the data that we eventually want in our processed config file. the structure in this repo is as follows.  

```bash
configs
├── base
│   └── global.yaml - global defaults
├── customers
│   ├── customer1.yaml
│   └── customer2.yaml - customer specific file with customer deployment specific overrides
└── envs
    └── development.yaml - environment specific file with environment overrides
```

2. the `gitops` folder contains the gitops directory structure expected by tanzu. this is a folder per space and in that space a folder per app. This could live in another repo but for simplicity it is in the same as the configs. The directory structure is as follows. every app folder will contain an `ini_config.yml` that holds two key pieces of info, the environment name and the customer name. these could really be anything you want but that is what is used in this example. these two pieces of data are used to determine which files to layer for generating the config. This directory structure is also where the generate configs as well as the app manifests etc. will be placed. it is essentially the source for what lands in the space.

```bash
gitops
└── project
    └── spaces 
        ├── customer1
        │   └── my-app
        │       ├── ini-sectret.yml - generated config secret
        │       └── ini_config.yml - contains env/customer values for generation
        └── customer2
            └── my-app
                ├── ini-sectret.yml - generated config secret
                └── ini_config.yml - contains env/customer values for generation
```


3. a github action watches the `configs` directory for changes and runs the `scripts/generate.py` when any files change. this script loops over all of the spaces and finds the `ini_config.yml` which it uses to then construct the command that templates out the ini file. the script uses YTT to template the k8s secret that contains the ini file, the ytt template is in `ytt/ini-generate.yml`. This ytt command passes the layered configs in order of precedence. so startting with base, then env, customer, which means it is handling the overrides for us automatically. the files are then generated and placed in the correct app directories.

4. finally the github action commits these to a branch and opens a PR for review.

5. in a real world scenrario once these are commited they would be synced to the space using your favorite gitops tool. 