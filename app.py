from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

app = Flask(__name__)
CORS(app)

# Load the finetuned T5 model
model_name = "mrm8488/t5-base-finetuned-common_gen"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Fallback dictionary for hard words
fallback_dict = {
    "endeavored": "tried",
    "commence": "start",
    "expeditiously": "quickly",
    "ameliorate": "improve",
    "terminate": "end",
    "utilize": "use",
    "comprehend": "understand",
    "reside": "live",
    "facilitate": "help"
}

def simplify_with_fallback(text, simplified):
    explanation = []
    original_words = text.split()
    simplified_words = simplified.split()

    if simplified.lower() == text.lower() or simplified.strip() == "":
        for word in original_words:
            if word.lower() in fallback_dict:
                new_word = fallback_dict[word.lower()]
                simplified = simplified.replace(word, new_word)
                explanation.append({
                    "original": word,
                    "simplified": new_word,
                    "reason": f"Replaced '{word}' with fallback word '{new_word}'"
                })
        return simplified, explanation

    # If model simplification happened, compare and explain
    for o, s in zip(original_words, simplified_words):
        if o.lower() != s.lower():
            explanation.append({
                "original": o,
                "simplified": s,
                "reason": f"Replaced '{o}' with simpler word '{s}'"
            })

    return simplified, explanation


@app.route("/simplify", methods=["POST"])
def simplify():
    data = request.get_json()
    text = data.get("text", "")

    try:
        input_text = "simplify: " + text
        input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=128, truncation=True)
        output_ids = model.generate(input_ids, max_length=100, num_beams=4, early_stopping=True)
        simplified = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        simplified_text, explanation = simplify_with_fallback(text, simplified)

        return jsonify({
            "simplified_text": simplified_text,
            "explanation": explanation
        })

    except Exception as e:
        return jsonify({
            "simplified_text": text,
            "explanation": [{"error": f"Error during simplification: {str(e)}"}]
        })


if __name__ == '__main__':
    app.run(debug=True)