def read_questions_from_file(file_path):
    questions = []
    with open(file_path, 'r') as file:
        for line in file:
            question = line.strip()
            if question:
                questions.append(question)
    return questions

def write_answers_to_file(answers):
    with open('answers.txt', 'w') as file:
        for answer in answers:
            file.write(answer + '\n')

if __name__ == '__main__':
    questions = read_questions_from_file('form.txt')
    print(questions)