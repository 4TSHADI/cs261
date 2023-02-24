const questionContainer = document.getElementById("question-container");
const questionText = document.getElementById("question");
const answerBtns = document.getElementById("ans-btns");
const prevBtn = document.getElementById("prev-btn");

let questionNum = 0;

const questions = [
    {
        question: 'What do you find more important?',
        answers: [
            {text: 'A'},
            {text: 'B'},
            {text: 'Both'}
        ]
    },
    {
        question: 'What is 9 + 10',
        answers: [
            {text: '21'},
            {text: '19'},
            {text: 'yes'}
        ]
    }
]

nextQuestion();

prevBtn.addEventListener("click", () => {
    if (questionNum > 0) {
        questionNum--;
        nextQuestion();
    }
})

function nextQuestion() {
    removeBtns();
    displayQuestion(questions[questionNum]);
}

function selectAnswer(e) {
    if (questions.length <= questionNum) {
        window.location.href = "/profile";
    }
}

function removeBtns() {
    while (answerBtns.firstChild) {
        answerBtns.removeChild(answerBtns.firstChild);
    }
}

function displayQuestion(question) {
    questionText.innerText = question.question;
    question.answers.forEach(answer => {
        const btn = document.createElement("button");
        btn.innerText = answer.text;
        btn.classList.add("btn");
        btn.addEventListener("click", () => {
            questionNum++;
            nextQuestion();
        })

        btn.addEventListener("click", selectAnswer);
        answerBtns.appendChild(btn);
    });
}



