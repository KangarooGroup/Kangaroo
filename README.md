# Kangaroo: A Powerful Video-Language Model Supporting Long-context Video Input

## Release
- [2024/07/17] 🔥 **Kangaroo** has been released. We release [blog](https://kangaroogroup.github.io/Kangaroo.github.io/) and [model](https://huggingface.co/KangarooGroup/kangaroo). Please check out the blog for details.

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
