# This script is used to pre=download files stored with git-lfs in CML Runtimes which do not have git-lfs support
# You can use any models that can be loaded with the huggingface transformers library. See utils/model_embedding_utls.py or utils/moderl_llm_utils.py
EMBEDDING_MODEL_REPO="https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2"
EMBDEDDING_MODEL_COMMIT="9e16800aed25dbd1a96dfa6949c68c4d81d5dded"

CLOUDERA_KNOWLEDGE_BASE="https://github.com/kevinbtalbert/cloudera_knowledge_base.git"

download_lfs_files () {
    echo "These files must be downloaded manually since there is no git-lfs here:"
    git ls-files | git check-attr --stdin filter | awk -F': ' '$3 ~ /lfs/ { print $1}' | while read line; do 
        echo $(git remote get-url $(git remote))/resolve/$(git rev-parse HEAD)/${line}
        curl -O -L $(git remote get-url $(git remote))/resolve/$(git rev-parse HEAD)/${line}
    done
}

# Clear out any existing checked out models
rm -rf ./models
mkdir models
cd models

# Downloading model for generating vector embeddings
GIT_LFS_SKIP_SMUDGE=1 git clone ${EMBEDDING_MODEL_REPO} --branch main embedding-model 
cd embedding-model
git checkout ${EMBDEDDING_MODEL_COMMIT}
download_lfs_files
cd ..
  
# Downloading Cloudera Internal Knowledge base
cd ..
cd data
GIT_LFS_SKIP_SMUDGE=1 git clone ${CLOUDERA_KNOWLEDGE_BASE} --branch main
cd ..