import os
import streamlit as st
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM


@st.cache_resource
def init_model():
    tokenizer = AutoTokenizer.from_pretrained("KangarooGroup/kangaroo")
    model = AutoModelForCausalLM.from_pretrained(
        "KangarooGroup/kangaroo",
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    )
    model = model.to("cuda")
    terminators = [tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<|eot_id|>")]
    return tokenizer, model, terminators

def show_video():
    st.title('Kangraoo Chatbot')
    path_or_url = st.text_input('Please enter the video path or URL. You can also use one of the demo videos available in the ./demo_videos directory: bike.mp4, castle.mp4, robot.mp4, or winter.mp4.', value='demo_videos/bike.mp4')
    if path_or_url.strip() != '':
        if path_or_url.startswith('http'):
            video_path = f"demo_videos/{path_or_url.split('/')[-1]}"
            os.system(f'wget -c -O {video_path} {path_or_url}')
        else:
            video_path = path_or_url
            assert Path(video_path).exists()
        st.video(open(video_path, 'rb'))
    return video_path

def get_response(user_question, tokenizer, model, terminators, video_path):
    if user_question:
        if len(st.session_state.message) > 0:
            last_bot_message = st.session_state.message[-1]
            assert last_bot_message["role"] == "bot"
            history = last_bot_message["history"]
        else:
            history = None
        st.session_state.message.append({"role": "user", "content": user_question})
        response, history = model.chat(video_path=video_path,
                                query=user_question,
                                tokenizer=tokenizer,
                                max_new_tokens=512,
                                eos_token_id=terminators,
                                do_sample=True,
                                temperature=0.6,
                                top_p=0.9,
                                history=history)
        st.session_state.message.append({"role": "bot", "content": response, "history": history})
        return response
    return None

def display_history_conversation():
    for item in st.session_state.message:
        if item["role"] == "user":
            st.write(f":blue[**[User]:** {item['content']}]")
        else:
            st.write(f":green[**[Kangaroo]:** {item['content']}]")
      
def chat(tokenizer, model, terminators, video_path):
    if "message" not in st.session_state:
        st.session_state.message = []

    question_widget, send_button = st.columns([9,1], vertical_alignment='bottom')
    user_question = question_widget.text_input("Your question:", key="input")
    regen_button, clear_button = st.columns(2)
    # click Send button
    if send_button.button("Send", type="primary"):
        response = get_response(user_question, tokenizer, model, terminators, video_path)
        display_history_conversation()
    # click Regenerate button
    if regen_button.button("Regenerate"):
        st.session_state.message.pop()
        user_question = st.session_state.message[-1]["content"]
        st.session_state.message.pop()
        response = get_response(user_question, tokenizer, model, terminators, video_path)
        display_history_conversation()
    # click Clear history button
    if clear_button.button("Clear history"):
        st.session_state.message = []

            
if __name__ == "__main__":
    st.sidebar.image('assets/logo.png')
    tokenizer, model, terminators = init_model()
    video_path = show_video()
    chat(tokenizer, model, terminators, video_path)
