const questionContainer = document.getElementById("question-container");
const questionText = document.getElementById("question");
const answerBtns = document.getElementById("ans-btns");
const prevBtn = document.getElementById("prev-btn");
const controls = document.getElementById("controls");

const more = 3 // value for factors rated more significant
const less = 1/3 // value for factors rated less significant
const same = 1 // value for factors rated equally significant

let matrix = new Array(6).fill(0).map(() => new Array(6).fill(0));

for (index = 0; index < matrix.length; index++) { // factors compared against themselves have val 1
    matrix[index][index] = 1;
}

let questionNum = 0;

const factors = ["Size and experience level of team", "Satisfiability with work environment and project scope",
"Project budget", "Efficient time management and weekly hours of work","Quality of code and Git pull requests",
"Frequency and effectiveness of communication within team and with stakeholders"];

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

nextQuestion(false);

prevBtn.addEventListener("click", () => {
    if (questionNum > 0) {
        questionNum--;
        if (questionNum == 0){prevBtn.classList.add('hide');}
        nextQuestion(true);
    }
})

function nextQuestion(buttonPressed) {
    removeBtns();
    displayQuestion(questions[questionNum]);
    if (buttonPressed) {
        undoMatrix();
    }
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
    let opt1 = question.answers[0].text;
    let opt2 = question.answers[1].text;
    question.answers.forEach(answer => {
        const btn = document.createElement("button");
        btn.innerText = answer.text;
        btn.classList.add("btn");
        btn.addEventListener("click", () => {
            populateMatrix(opt1, opt2, btn.innerText);
            questionNum++;
            nextQuestion(false);
        });
    

        btn.addEventListener("click", selectAnswer);
        answerBtns.appendChild(btn);
    });
}

function populateMatrix(ans1, ans2, chosenAns) {
    let chosenIndex, otherIndex;
    if (chosenAns == "Both Equally") {
        indx1 = factors.indexOf(ans1);
        indx2 = factors.indexOf(ans2);
        matrix[indx1][indx2] = same;
        matrix[indx2][indx1] = same;      
        return ;
    }
    else if (chosenAns == ans1) {
        chosenIndex = factors.indexOf(ans1);
        otherIndex = factors.indexOf(ans2);
    }
    else {
        chosenIndex = factors.indexOf(ans2);
        otherIndex = factors.indexOf(ans1);
    }
    matrix[otherIndex][chosenIndex] = more;
    matrix[chosenIndex][otherIndex] = less;



    for (var row = 0; row < matrix.length; row++) {
        console.log(matrix[row]);
    }
    console.log("------------------------------------------");
}

function undoMatrix() {
    let question = questions[questionNum];
    indx1 = factors.indexOf(question.answers[0].text);
    indx2 = factors.indexOf(question.answers[1].text);
    matrix[indx1][indx2] = 0;
    matrix[indx2][indx1] = 0;
    // for (var row = 0; row < matrix.length; row++) {
    //     console.log(matrix[row]);
    // }
    // console.log("------------------------------------------");

}



