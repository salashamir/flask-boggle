class Boggle{
  // create new boggle game at whatever id is passed in
  constructor(boardId, seconds = 60){
    this.seconds = seconds;
    this.score = 0;
    this.words = new Set();
    this.board = $(`#${boardId}`);
    this.timer = setInterval(this.secondPass.bind(this), 1000);
    // form submission
    $('#word-form', this.board).on('submit', this.handleWordSubmit.bind(this));
  }

  showMessage(msg, cls){
    $('.msg', this.board).text(msg).removeClass().addClass(`msg ${cls}`);
  }

  showTimer(){
    $('#timer', this.board).text(this.seconds);
  }

  showScore(){
    $('#score', this.board).text(this.score);
  }

  showWord(word){
    $(".words", this.board).append($(`<li>${word}</li>`))
  }

  async secondPass(){
    this.seconds -= 1;
    this.showTimer();

    if(!this.seconds){
      clearInterval(this.timer);
      await this.finalScore();
    }
  }

  async finalScore(){
    $('.word-form', this.board).hide();
    const res = await axios.post("/post-score", {score: this.score});
    if(res.data.brokeRecord){
      this.showMessage(`NEW RECORD! ${this.score}`, "ok");
    } else {
      this.showMessage(`Final Score: ${this.score}`, "ok");
    }
  }

  async handleWordSubmit(e){
    e.preventDefault();
    // query for word dom input
    const $word = $('#word');
    // get value
    const word = $word.val();
    // check for emptty input
    if(!word) return;
    // check global set for duplicate
    if(this.words.has(word)){
      this.showMessage(`You've already found ${word}`, "err");
      return;
    };
    // check server
    const res = await axios.get("/check-word", {params:{word:word}})
    console.log(res.data);
    // get data payload
    const data = res.data;
  
    if(data.result === "not-on-board"){
      this.showMessage(`${word} is not on this board`, 'err');
    } else if (data.result === "not-word"){
      this.showMessage(`${word} is not an English word`, 'err');
    } else {
      this.showWord(word);
      this.score += word.length;
      this.showScore();
      this.words.add(word);
      this.showMessage(`Added ${word}`, 'ok');
    }

    $word.val("");
  };
}

const boggleGame = new Boggle('boggle-game', 50);

