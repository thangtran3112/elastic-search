# ElasticSearch with Python

## YouTube series

In this YouTube series, we explain some concepts in details. Each video corresponds to specific notebooks. The notebooks have a prefix in this format `<video_number>_notebook_name`, for example `3_create_index` corresponds to the 3rd video in the series.

[Watch the ElasticSearch Python tutorial series](https://www.youtube.com/watch?v=U3EUBGMVWZ4&list=PLMSb3cZXtIfpiHVLwXhaWk3KDXuklHdj5)

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

* Accessing ElasticSearch inside container

```zsh
  sudo docker start elasticsearch
  sudo docker exec -u 0 -it elasticsearch bash
```

After logging into the elasticsearch container, we can change the heap size, by creating `heap.option` file inside `jvm.options.d` folder:

For instance, using `-Xms2g` for `2GB of RAM`:

```bash
echo "-Xms2g" > /usr/share/elasticsearch/config/jvm.options.d/heap.options
echo "-Xmx2g" >> /usr/share/elasticsearch/config/jvm.options.d/heap.options

# Checking and restart
cat /usr/share/elasticsearch/config/jvm.options.d/heap.options
sudo docker restart elasticsearch
```
