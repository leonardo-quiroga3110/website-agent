import os

def analyze():
    log_path = 'test_refinement_results.log'
    if not os.path.exists(log_path):
        print("Log not found.")
        return

    with open(log_path, 'rb') as f:
        content = f.read().decode('utf-16', errors='ignore')

    # Print interesting parts
    sections = content.split('--- TEST:')
    for section in sections[1:]:
        header, body = section.split('\n', 1)
        print(f"### TEST: {header.strip()}")
        
        # Extract Answer
        if 'Answer:' in body:
            answer_start = body.find('Answer:') + 7
            answer_end = body.find('--------------------------------------------------', answer_start)
            answer = body[answer_start:answer_end].strip()
            print(f"**Answer (Length: {len(answer)} chars):**\n{answer}\n")
            
        # Extract Visited
        if 'Visited:' in body:
            visited_start = body.find('Visited:') + 8
            visited_end = body.find('\n', visited_start)
            visited = body[visited_start:visited_end].strip()
            print(f"**Visited:** {visited}\n")

if __name__ == "__main__":
    analyze()
