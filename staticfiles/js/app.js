const questionNumber = document.querySelector(".question-number");
const questionText = document.querySelector(".question-text");
const optionContainer = document.querySelector(".option-container");
const answersIndicatorContainer = document.querySelector(".answers-indicator");
const homeBox = document.querySelector(".home-box");
const quizBox = document.querySelector(".quiz-box");
const resultBox = document.querySelector(".result-box");

let questionCounter = 0;
let currentQuestion;
let availableQuestions = [];
let availableOptions = [];
let correctAnswers =0;
let attempt =0;

// Push the questions into availableQuestions
function setAvailableQuestions() {
    const totalQuestions = quiz.length;
    for (let i = 0; i < totalQuestions; i++) {
        availableQuestions.push(quiz[i]);
    }
}

// set question number and question and options
function getNewQuestion() {
    // set question number
    questionNumber.innerHTML = "Question " + (questionCounter + 1) + " of " + quiz.length;

    // Get random question
    const questionIndex = availableQuestions[Math.floor(Math.random() * availableQuestions.length)];
    currentQuestion = questionIndex;
    questionText.innerHTML = currentQuestion.q;

    // Remove the question from availableQuestions to avoid repetition
    const index1 = availableQuestions.indexOf(questionIndex);
    availableQuestions.splice(index1, 1);

    // Reset availableOptions for the new question
    availableOptions = [];

    // Set options
    const optionLen = currentQuestion.Option.length;
    for (let i = 0; i < optionLen; i++) {
        availableOptions.push(i);
    }
    optionContainer.innerHTML =' ';
    let animationDelay = 0.15;

    // Create options in HTML
    optionContainer.innerHTML = ''; // Clear previous options
    for (let i = 0; i < optionLen; i++) {
        // random options
        const optionIndex =availableOptions[Math.floor(Math.random() * availableOptions.length)];
        // get the position of 'optionIndex' from the availableoptions
        const index2 =availableOptions.indexOf(optionIndex);
        // remove the 'optionIndex' from the availableoptions , so that the option does not repeat
        availableOptions.splice(index2,1);
        
        const option = document.createElement("div");
        option.innerHTML = currentQuestion.Option[optionIndex];
        option.id = optionIndex;
        option.style.animationDelay = animationDelay + 's';
        animationDelay = animationDelay + 0.15;
        option.className = "option";
        
        optionContainer.appendChild(option);
        option.setAttribute("onclick", "getResult(this)");
    }

    questionCounter++;
}

// get the result of current attempt question
function getResult(element){
    const id =parseInt(element.id);
    // get the answer by comparing the correct attempt question
    if(id === currentQuestion.answer){
        // get the green color to the correct option
        element.classList.add("correct");
        // add the indicator to the correct marks
        updateAnswerIndicator("correct");
        correctAnswers++;
    }else{
         // get the RED color to the incorrect option
         element.classList.add("wrong");
          // add the indicator to the wrong marks
        updateAnswerIndicator("wrong");

        //  if the answer is incorrect this show the correct option by adding green color to the correct option
        const optionLen = optionContainer.children.length;
        for(let i=0 ; i< optionLen ; i++){
            if( parseInt(optionContainer.children[i].id) === currentQuestion.answer){
                optionContainer.children[i].classList.add("correct");
            }
        }
    }
    attempt++;
    unclickableOptions();
}
// make all the options unclickable once the user select a option (RESTRICT THE USER TO CHANGE THE OPTION)
function unclickableOptions(){
    const optionLen = optionContainer.children.length;
    for (let i=0 ; i<optionLen ; i++){
        optionContainer.children[i].classList.add("already-answered");
    }
}
function answersIndicator(){
    answersIndicatorContainer.innerHTML = '';
    const totalQuestion = quiz.length;
    for( let i=0 ; i<totalQuestion ; i++){
        const indicator = document.createElement("div");
        answersIndicatorContainer.appendChild(indicator);
    }
}
function updateAnswerIndicator(marktype){
    answersIndicatorContainer.children[questionCounter-1].classList.add(marktype)
}


// Handle Next Question
function next() {
    if (questionCounter === quiz.length) {
        quizOver();
    } else {
        getNewQuestion();
    }
}
function quizOver(){
    // hide quiz quizBox
    quizBox.classList.add("hide")
    // show result box
    resultBox.classList.remove("hide");
    quizResult();
}
// get the quiz result
    function quizResult(){
        resultBox.querySelector(".total-question").innerHTML = quiz.length;
        resultBox.querySelector(".total-attempt").innerHTML = attempt;
        resultBox.querySelector(".total-correct").innerHTML = correctAnswers;
        resultBox.querySelector(".total-wrong").innerHTML =attempt - correctAnswers;
        const percent = (correctAnswers/quiz.length)*100;
        resultBox.querySelector(".percentage").innerHTML = percent.toFixed(2) + "%";
        resultBox.querySelector(".total-score").innerHTML = correctAnswers + " / " + quiz.length;
    }
    function resetQuiz(){
       questionCounter = 0;
       correctAnswers =0;
       attempt =0;
    }

    function tryAgainQuiz(){
        // hide the resultBox
        resultBox.classList.add("hide");
        // show the quizBox
        quizBox.classList.remove("hide");
        resetQuiz();
        startQuiz();
    }
    function goToHome(){
        // hide resultBox
        resultBox.classList.add("hide");
        // show resultBox
        homeBox.classList.remove("hide");
        resetQuiz();

    }


// #### STARTING POINT ####
function startQuiz() {
    // hide home box
    homeBox.classList.add("hide");
    // show quiz box
    quizBox.classList.remove("hide");
    // first we will set all questions in availableQuestions array
    setAvailableQuestions();
    //  second we will call getNewQuestion() function
    getNewQuestion(); 
// to create indicator of answers
answersIndicator();
}

window.onload= function (){
    homeBox.querySelector(".total-question").innerHTML = quiz.length;
}
