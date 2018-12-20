workflow "Deploy Dataset Schema" {
  on = "push"
  resolves = ["Extract Dataset Schema"]
}

action "list" {
  uses = "actions/bin/sh@master"
  runs = "ls"
  args = ["/github/workspace"]
}

action "Extract Dataset Schema" {
  needs = ["list"]
  uses = "docker://openschemas/extractors:Dataset"
  secrets = ["GITHUB_TOKEN"]
  env = {
    DATASET_THUMBNAIL = "https://vsoch.github.io/datasets/assets/img/avocado.png"
    DATASET_ABOUT = "Images and metadata from ~10K Github repositories. A Dinosaur Dataset. See https://vsoch.github.io/2018/extension-counts/"
    DATASET_DESCRIPTION = "Data is compressed with squashfs and includes python3 pickled images and metadata dictionaries. "
    CONTACT_URL = "https://www.github.com/vsoch/zenodo-ml/issues"
  }
  args = ["extract", "--name", "zenodo-ml", "--contact", "@vsoch", "--version", "1.0.0", "--deploy"]
}
