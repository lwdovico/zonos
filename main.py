import torch
import torchaudio
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict
from zonos.utils import DEFAULT_DEVICE as device

from pydub import AudioSegment

from tqdm import tqdm
import argparse
import tempfile
import re
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-text", type=str)
    parser.add_argument("--speaker", type=str, default="assets/exampleaudio.mp3")
    parser.add_argument("--language", type=str, default="en-us")
    parser.add_argument("--output-path", type=str, default="/app/outputs/output.mp3")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device=device)

    wav, sampling_rate = torchaudio.load(args.speaker)
    speaker = model.make_speaker_embedding(wav, sampling_rate)

    torch.manual_seed(args.seed)
    
    if os.path.exists(args.input_text):
        print("Reading from file")
        with open(args.input_text, "r") as f:
            source_text = f.read()
    elif ' ' in args.input_text or '\n' in args.input_text:
        print("Reading from string")
        source_text = args.input_text

    texts = [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+', source_text) if s.strip()]

    merged_audio = AudioSegment.silent(duration=0)

    for sentence in tqdm(texts):
        cond_dict = make_cond_dict(text=sentence, speaker=speaker, language=args.language)
        conditioning = model.prepare_conditioning(cond_dict)
        codes = model.generate(conditioning, progress_bar = False)
        wavs = model.autoencoder.decode(codes).cpu()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            torchaudio.save(f.name, wavs[0], model.autoencoder.sampling_rate)
            merged_audio += AudioSegment.from_wav(f.name) + AudioSegment.silent(duration=500)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        merged_audio.export(f.name, format='mp3')
        print("Normalizing audio...")
        os.system(f'mkdir -p "$(dirname {args.output_path})" && ffmpeg -i {f.name} -af "loudnorm" {args.output_path}')
