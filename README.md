# Zonos Basic Setup with Multiple Sentence Inference

This repository provides a basic setup for using [Zonos](https://github.com/Zyphra/Zonos), a text-to-speech model designed for generating audio in mutiple languages. This small framework allows for seamless text-to-speech conversion beyond the 30 seconds default limit.

## Features

- **Multi-sentence processing**: Converts multiple sentences of input text into audio.
- **Flexible input options**: Accepts both text files and direct input strings.
- **Audio normalization**: Automatically normalizes the generated audio for better sound quality.
- **Output formats**: Supports generating audio in MP3 format.
- **Gradio Interface**: Inference can be run both via .py or via the gradio interface (reccomended).
  
## Requirements

- Docker
- A nvidia GPU with +6GB VRAM

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lwdovico/zonos
   cd zonos
   ```
2. Then you can build and launch the gradio interface (reccomended):
   ```bash
   docker compose up
   ```
3. Open the Gradio UI at: http://localhost:7861/

NB: The docker exposes the port 7861, if you need to change it please be sure to update it also in the gradio_main.py

### Optional: Build manually

You don't need to do it if you want to use the Gradio WebUI only

1. Build the container:
```bash
   docker build -t zonos .
   ```
Optionally add your assets to the path before building the docker so to have them mounted

2. Run and attach to it:
```bash
   docker run -it --gpus=all --net=host -v /path/to/zonos_outputs:/app/outputs -t zonos
```

#### Running manually the Inference

To generate audio from text, run the following script:

```bash
python main.py --input-text "Your text here."
```

You can also provide a path if the text is too long for the command line:

```bash
python main.py --input-text /path/to/text.txt
```

This will process the text and output a single audio file.

#### Customizing the Setup

NB: It doesn't allow for all the customizations available in the Gradio WebUI

You can customize the behavior of the script by adding the following command-line arguments:

- `--input-text`: Specifies the text you want to convert into speech. Provide the text directly as a string or a path.
- `--speaker`: Defines the speaker to use for the audio generation. By default, it uses an example audio file (`assets/exampleaudio.mp3`), but you can specify your own file or speaker model.
- `--language`: Sets the language for the audio. The default is English (`en-us`), but you can change it to another supported language code.
- `--output-path`: Determines where the generated audio will be saved. The default output file is `output.mp3`, but you can specify a custom path or filename (only absolute paths). Set the mounted output path `/app/outputs/output.mp3` to have them in the `/path/to/zonos_outputs`
- `--seed`: Sets a random seed for reproducibility of the results. The default is `42`, but you can modify it if needed.

Example usage:

```bash
python main.py --input-text "Hello world!" --speaker "another_speaker.mp3" --language "fr-fr" --output-path "french_output.mp3" --seed 1234
```

## Acknowledgements
Special thanks to the Zonos developers for creating this text-to-speech model.
