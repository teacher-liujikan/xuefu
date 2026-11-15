import numpy as np,soundfile as sf
from piper import PiperVoice
V=PiperVoice.load('/home/claude/work/audio/tts/vits-piper-en_US-amy-medium/en_US-amy-medium.onnx')
SR=V.config.sample_rate
def say(t,speed=1.15):
    from piper import SynthesisConfig
    cfg=SynthesisConfig(length_scale=speed)
    return np.concatenate([c.audio_float_array for c in V.synthesize(t,syn_config=cfg)])
def build(parts,out):
    seg=[np.zeros(int(SR*0.3),dtype=np.float32)]
    for p in parts:
        seg.append(np.zeros(int(SR*p),dtype=np.float32) if isinstance(p,(int,float)) else say(p))
    seg.append(np.zeros(int(SR*0.4),dtype=np.float32))
    sf.write(out,np.concatenate(seg),SR)
