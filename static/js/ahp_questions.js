const questionContainer = document.getElementById("question-container");
const questionText = document.getElementById("question");
const answerBtns = document.getElementById("ans-btns");
const prevBtn = document.getElementById("prev-btn");
const controls = document.getElementById("controls");



let questionNum = 0;

const questions = [
    {
        question: 'Which aspect do you value more in your team project?',
        answers: [
            {text: "Size and experience level of team"},
            {text: "Satisfiability with work environment and project scope"},
            {text: "Both Equally"}
        ]
    },
    {
        question: 'Which aspect do you value more in your team project?',
        answers: [
            {text: "Size and experience level of team"},
            {text: "Project budget"},
            {text: "Both Equally"}
        ]
    },
    {
        question: "Which aspect do you value more in your team project?",
        answers: [
            {text: "Size and experience level of team"},
            {text: "Efficient time management and weekly hours of work"},
            {text: 'Both Equally'}
        ]
    },
    {
        question: "Which aspect do you value more in your team project?",
        answers: [
            {text: "Size and experience level of team"},
            {text: "Quality of code and Git pull requests"},
            {text: "Both Equally"}
        ]
    },
    {
        question: "Which aspect do you value more in your team project?",
        answers: [
            {text: "Size and experience level of team"},
            {text: "Frequency and effectiveness of communication within team and with stakeholders"},
            {text: "Both Equally"}
        ]
    },
    {
        question: 'Which aspect do you value more in your team project?',
        answers: [
            {text: "Satisfiability with work environment and project scope"},
            {text: "Project budget"},
            {text: "Both Equally"}
        ]
    },
    {
        question: "Which aspect do you value more in your team project?",
        answers: [
            {text: "Satisfiability with work environment and project scope"},
            {text: "Efficient time management and weekly hours of work"},
            {text: "Both Equally"}
        ]
    },
    {
        question: "Which aspect do you value more in your team project?",
        answers: [
            {text: "Satisfiability with work environment and project scope"},
            {text: "Quality of code and Git pull requests"},
            {text: "Both Equally"}
        ]
    },
    {
        question: "Which aspect do you value more in your team project?",
        answers: [
            {text: "Satisfiability with work environment and project scope"},
            {text: "Frequency and effectiveness of communication within team and with stakeholders"},
            {text: "Both Equally"}
        ]
    },
    {
        question: "Which aspect do you value more in your team project?",
        answers: [
            {text: "Project budget"},
            {text: "Efficient time management and weekly hours of work"},
            {text: "Both Equally"}
        ]
    },
    {
        question: "Which aspect do you value more in your team project?",
        answers: [
            {text: "Project budget"},
            {text: "Quality of code and Git pull requests"},
            {text: "Both Equally"}
        ]
    },
    {
        question: "Which aspect do you value more in your team project?",
        answers: [
            {text: "Project budget"},
            {text: "Frequency and effectiveness of communication within team and with stakeholders"},
            {text: "Both Equally"}
        ]
    },
    {
        question: "Which aspect do you value more in your team project?",
        answers: [
            {text: "Efficient time management and weekly hours of work"},
            {text: "Quality of code and Git pull requests"},
            {text: "Both Equally"}
        ]
    },
    {
        question: "Which aspect do you value more in your team project?",
        answers: [
            {text: "Efficient time management and weekly hours of work"},
            {text: "Frequency and effectiveness of communication within team and with stakeholders"},
            {text: "Both Equally"}
        ]
    },
    {
        question: "Which aspect do you value more in your team project?",
        answers: [
            {text: "Quality of code and Git pull requests"},
            {text: "Frequency and effectiveness of communication within team and with stakeholders"},
            {text: "Both Equally"}
        ]
    }
]

nextQuestion();

prevBtn.addEventListener("click", () => {
    if (questionNum > 0) {
        questionNum--;
        if (questionNum == 0){prevBtn.classList.add('hide');}
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
    if (questionNum > 0){
        prevBtn.classList.remove('hide');
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
        });
    

        btn.addEventListener("click", selectAnswer);
        answerBtns.appendChild(btn);
    });
}



