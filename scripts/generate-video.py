
from flask import Flask, request, send_file
import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
import subprocess

global mpv_process
mpv_process = None

app = Flask(__name__)

pipe = DiffusionPipeline.from_pretrained("cerspense/zeroscope_v2_576w", torch_dtype=torch.float16)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_model_cpu_offload()

@app.route('/generate', methods=['POST'])
def generate_video():
    global mpv_process

    prompt = request.json['prompt']
    video_frames = pipe(prompt, num_inference_steps=60, height=168, width=304, num_frames=24).frames
    video_path = export_to_video(video_frames, fps=8)
    video_name = video_path.replace('/tmp', '')

    if mpv_process is not None:
        mpv_process.kill()
    mpv_process = subprocess.Popen(['mpv', '--loop', video_path])

    return {
        "success": True
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)