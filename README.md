# Kangaroo: A Powerful Video-Language Model Supporting Long-context Video Input

## Release
- [2024/07/17] 🔥 **Kangaroo** has been released. We release [blog](https://kangaroogroup.github.io/Kangaroo.github.io/) and [model](https://huggingface.co/KangarooGroup/kangaroo). Please check out the blog for details.

## Abstract
We introduce <strong>Kangaroo</strong>, a powerful Multimodal Large Language Model designed for long-context video understanding. Our presented Kangaroo model shows remarkable performance across diverse video understanding tasks including video caption, QA and conversation. Generally, our key contributions in this work can be summarized as follows:
<ol>
    <li><strong>Long-context Video Input.</strong> To enhance the model's capability to comprehend longer videos, we extend the maximum frames of input videos to 160. To this end, we aggregate multiple videos with variable frame counts and aspect ratios into one sample. We further design a spatial-temporal pathify module to improve training efficiency.</li>
    <li><strong>Strong Performance.</strong> We evaluate our model across various video understanding benchmarks. The results indicate that our model achieves state-of-the-art performance on the majority of comprehensive benchmarks and maintain a competitive level in others. Notably, our model outperforms most larger open-source models with over 30B parameters and some proprietary models on certain benchmarks.</li>
    <li><strong>Video Annotation System.</strong> We develop a data curation and automatic annotation system to generate captions for open-source and internal videos. The generated large-scale dataset are utilized for video-text pre-training. For video instruction tuning stage, we construct a video instruciton tuning dataset based on public and internal datasets covering a variety of tasks.</li>
    <li><strong>Billingual Conversation.</strong> Our proposed model is equipped with the capability of Chinese, English and billingual conversations, and support single/multi-round conversation paradigms.
    </li>
</ol>

## Model
<p align="center">
    <img src="demo/model.png" width="50%" style="margin-top: 40px;">
</p>

## Quick Start

### Requirements
- python == 3.9
- torch == 2.1.0, torchvision == 0.16.0
- CUDA == 12.1 (for GPU)
- transformers == 4.41.0
- xformers == 0.0.23

### Simple use with 🤗 Transformers
```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("KangarooGroup/kangaroo")
model = AutoModelForCausalLM.from_pretrained(
    "KangarooGroup/kangaroo",
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
)
model = model.to("cuda")
terminators = [tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<|eot_id|>")]

video_path = "path/to/video"
query = "Please describe this video"
out, history = model.chat(video_path=video_path,
                          query=query,
                          tokenizer=tokenizer,
                          max_new_tokens=512,
                          eos_token_id=terminators,
                          do_sample=True,
                          temperature=0.6,
                          top_p=0.9,)
print(out) 

query = "What happend at the end of the video?"
out, history = model.chat(video_path=video_path,
                          query=query,
                          history=history,
                          tokenizer=tokenizer,
                          max_new_tokens=512,
                          eos_token_id=terminators,
                          do_sample=True,
                          temperature=0.6,
                          top_p=0.9,)
print(out)
```

## Results
<p align="center">
    <img src="demo/bench.png" width="50%" style="margin-top: 40px;">
</p>
<p align="center">
    <img src="demo/demo1.png" width="50%" style="margin-top: 40px;">
</p>
<p align="center">
    <img src="demo/demo2.png" width="50%" style="margin-top: 40px;">
</p>

## Citation

If you find it useful for your research , please cite related papers/blogs using this BibTeX:
```bibtex

@misc{kangaroogroup,
	title={Kangaroo: A Powerful Video-Language Model Supporting Long-context Video Input},
	url={https://kangaroogroup.github.io/Kangaroo.github.io/},
	author={Jiajun Liu and Yibing Wang and Hanghang Ma and Xiaoping Wu and Xiaoqi Ma and Jie Hu},
	month={July},
	year={2024}
}
