```
npx cdk init app --language python
rm -rf .venv/
rm requirements*
rm source.bat
```

```
conda create -n py_wuuurms python=3.12
conda activate py_wuuurms
```

```
poetry init
```

Output:
```
[tool.poetry]
name = "wuuurms-infra"
version = "0.1.0"
description = "infra of wuuurms"
authors = ["JelsB <boulangier.jels@gmail.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "~3.12"
aws-cdk-lib = "~2.161.1"
constructs = "~10.3.0"


[tool.poetry.group.dev.dependencies]
pytest = "~8.3.3"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

```
poetry add --group=dev ruff
```

Update cdk.json `app` command
