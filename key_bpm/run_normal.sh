docker run \
-v ./src:/src \
-v ~/Music/play:/play \
-t bpmkey:latest \
python add_key_and_bpm.py