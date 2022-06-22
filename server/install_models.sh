mkdir models
cs models
wget https://github.com/bjascob/amrlib-models/releases/download/model_parse_t5-v0_2_0/model_parse_t5-v0_2_0.tar.gz
tar xzf model_parse_t5-v0_2_0.tar.gz
ln -snf model_parse_t5-v0_2_0 model_stog
pip install protobuf==3.20.*
