import json
import re

# Your JSON string
json_string = '''
{
        "url": "https://khoahoc.vietjack.com/thi-online/20-cau-trac-nghiem-toan-12-canh-dieu-bai-1-tinh-don-dieu-cua-ham-so-co-dap-an/146828\\n",
        "question": "I. Nh\\u1eadn bi\\u1ebft\\nCho \\u0111\\u1ed3 th\\u1ecb h\\u00e0m s\\u1ed1 b\\u1eadc ba f(x)=ax3+bx2+cx+df(x)=ax3+bx2+cx+d c\\u00f3 b\\u1ea3ng x\\u00e9t d\\u1ea5u nh\\u01b0 h\\u00ecnh v\\u1ebd b\\u00ean d\\u01b0\\u1edbi.\\nH\\u00e0m s\\u1ed1 \\u0111\\u00e3 cho \\u0111\\u1ed3ng bi\\u1ebfn tr\\u00ean kho\\u1ea3ng n\\u00e0o sau \\u0111\\u00e2y?\\nA. (0;+\\u221e).(0;+\\u221e).\\nB. (\\u2212\\u221e;\\u22122).(\\u2212\\u221e;\\u22122).\\nC. (\\u22123;1).(\\u22123;1).\\nD. (\\u22122;0).(\\u22122;0).",
        "options": [
            "A. $$(0; + \\\\infty ).$$",
            "B. $$( - \\\\infty ; - 2).$$",
            "C. $$( - 3;1).$$",
            "D. $$( - 2;0).$$"
        ],
        "image": "https://video.vietjack.com/upload2/quiz_source1/2024/10/blobid0-1728868566.png",
        "answer": "\\u0110\\u00e1p \\u00e1n \\u0111\\u00fang l\\u00e0: D\\nD\\u1ef1a v\\u00e0o b\\u1ea3ng x\\u00e9t d\\u1ea5u, ta c\\u00f3 h\\u00e0m s\\u1ed1 \\u0111\\u1ed3ng bi\\u1ebfn tr\\u00ean kho\\u1ea3ng (\\u22122;0).(\\u22122;0)."
    }
'''

# Parse the JSON
data = json.loads(json_string)

# Function to clean and format for plain text with LaTeX
def format_text(text):
    # Fix polynomial notation
    text = re.sub(r'f\(x\)=ax3\+bx2\+cx\+d', r'f(x)=ax^3+bx^2+cx+d', text)
    
    # Replace duplicate text
    text = re.sub(r'f\(x\)=ax3\+bx2\+cx\+df\(x\)=ax3\+bx2\+cx\+d', r'f(x)=ax^3+bx^2+cx+d', text)
    
    # Remove duplicate intervals
    text = re.sub(r'\(([^)]+)\)\.\(([^)]+)\)', r'(\1)', text)
    
    return text

# Format the question
question = format_text(data["question"])

# Format the options
options = []
for option in data["options"]:
    # Remove extra $$ if they exist
    option_text = option.replace('$$', '$')
    # Convert LaTeX commands properly
    option_text = option_text.replace('\\infty', '∞')
    options.append(option_text)

# Format the answer
answer = format_text(data["answer"])

# Create the plain text output
plain_text = f"""
Question:
{question}

Options:
{options[0]}
{options[1]}
{options[2]}
{options[3]}

Answer:
{answer}

Image URL: {data["image"]}
"""

print(plain_text)

# Save to a file
with open("math_question.txt", "w", encoding="utf-8") as f:
    f.write(plain_text)

print("\nPlain text has been saved to 'math_question.txt'")