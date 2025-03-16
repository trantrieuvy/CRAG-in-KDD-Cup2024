import json
import re

def extract_final_answer(prediction_text):
    """
    Extract the final answer from the prediction text by removing any interim "thought" or "step" text.

    The logic is as follows:
      1) Look for a final answer in the format `\boxed{...}`.
      2) Look for "## Final Answer\n" and extract everything that follows.
      3) Look for phrases like "The final answer is" or "The answer is".
      4) If no markers are found, return the last sentence or a reasonable portion of the text.
    """
    # 1) Look for a final answer in the format `\boxed{...}`
    boxed_answer_pattern = r"\\boxed\{([^}]+)\}"
    match = re.search(boxed_answer_pattern, prediction_text)
    if match:
        return match.group(1).strip()

    # 2) Look for "## Final Answer\n"
    final_answer_marker = "## Final Answer\n"
    idx = prediction_text.find(final_answer_marker)
    if idx != -1:
        return prediction_text[idx + len(final_answer_marker) :].strip()

    # 3) Look for phrases like "The final answer is" or "The answer is"
    final_answer_phrases = [
        "the final answer is",
        "the answer is",
        "the correct answer is",
        "the symbol is",
        "the constellation is",
    ]
    for phrase in final_answer_phrases:
        lower_text = prediction_text.lower()
        idx = lower_text.find(phrase)
        if idx != -1:
            # Extract everything after the phrase
            return prediction_text[idx + len(phrase) :].strip()

    # 4) Fallback: Return the last sentence or a reasonable portion of the text
    sentences = re.split(r"[.!?]\s+", prediction_text)
    if sentences:
        return sentences[-1].strip()

    # If all else fails, return the original text
    return prediction_text.strip()

def process_json_lines(input_file, output_file):
    """
    Reads each line from `input_file` as JSON, processes its 'prediction' field using
    `extract_final_answer`, and writes the updated JSON line to `output_file`.
    """
    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:

        for line in fin:
            line = line.strip()
            if not line:
                # Skip empty lines
                continue

            # Safely parse the line as JSON
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                # If a line is not valid JSON, re-write it unchanged
                fout.write(line + "\n")
                continue

            # Clean up the 'prediction' field if present
            if 'prediction' in record:
                record['prediction'] = extract_final_answer(record['prediction'])

            # Write the updated record back as a JSON line
            fout.write(json.dumps(record, ensure_ascii=False) + "\n")


# # Example input line
# input_line = '{"query": "what is the most active volcano in the philippines?", "ground_truth": "mayon volcano", "prediction": "## Thought\nThe question asks for the most active volcano in the Philippines. To answer this, we need to look at the information provided in the references. Multiple documents mention that Mt. Mayon is considered the most active volcano in the Philippines, with one document stating it is \"also the most active volcano in the Philippines\" due to its frequent eruptions and perfect conical shape. Other volcanoes like Taal, Kanlaon, Bulusan, and Ragang are also mentioned as active, but Mt. Mayon is specifically highlighted as the most active.\n\n## Final Answer\nMt. Mayon"}'

# # Simulate processing the line
# record = json.loads(input_line)
# record['prediction'] = extract_final_answer(record['prediction'])
# processed_line = json.dumps(record, ensure_ascii=False)

# print(processed_line)
# Example usage:
process_json_lines('results/llama3.3:70b_predictions_new_prompts_task2.jsonl', 'output1.jsonl')
