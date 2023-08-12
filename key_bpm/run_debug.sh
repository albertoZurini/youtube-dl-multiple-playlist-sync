docker run \
-v ./src:/src \
-v ~/Music/play:/play \
-p 5678:5678 \
-t bpmkey:latest \
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client add_key_and_bpm.py