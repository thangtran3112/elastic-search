# ElasticSearch with Python

## [Installation ElasticSearch with Docker](https://www.elastic.co/search-labs/tutorials/install-elasticsearch/docker)

* Install and start elastic search with `trial` license, we can switch to `basic` license later on

```zsh
  sudo mkdir -p /Users/ttran/personal/elastic-search/volume
  sudo ls -ld /Users/ttran/personal/elastic-search/volume
```

```zsh
    sudo docker run -p 127.0.0.1:9200:9200 -d --name elasticsearch \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    -e "xpack.license.self_generated.type=trial" \
    -e "ES_JAVA_OPTS=-XX:UseSVE=0" \
    -e "CLI_JAVA_OPTS=-XX:UseSVE=0" \
    -v "elasticsearch-data:/Users/ttran/personal/elastic-search/volume" \
    docker.elastic.co/elasticsearch/elasticsearch:8.15.0
```

* See elasticsearch [issue with M4 Apple processor](https://discuss.elastic.co/t/issue-with-elasticsearch-docker-deployment-on-apple-silicon-m4-processor-macos-15-2/373214), which requires     `-e "ES_JAVA_OPTS=-XX:UseSVE=0"` and `-e "CLI_JAVA_OPTS=-XX:UseSVE=0"`

* This docker command will install eleastic search at `localhost:9200`. [Verify it](http://localhost:9200)

* Useful docker commands

```zsh
  docker image ls
  docker image rm <Image_Id>
  docker ps -a
  docker rm elasticsearch
  docker rmi docker.elastic.co/elasticsearch/elasticsearch:8.15.0
```

## Install Python with Anaconda

* Installing at default location `envs`:

```zsh
  conda create -n elastic_search python=3.11 
  conda activate elastic_search
```

```zsh
  conda env remove -n elastic_search
```

* Installing the environment exactly at a specify path (Preferrable)

```zsh
  conda create -p venv python=3.11
  conda activate venv/
```

* Installing `elasticsearch` python client:

```zsh
  pip install -r requirements.txt
```
