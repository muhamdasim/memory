let socket = null;
let dot = {};
let settings = {
  size: 30,
  speed: 250,
  bg: '#FFFFFF',
  mode: 'emdr-linear',
  color: false,
  sound: ""
};
let isRunning = false;
let randomIdx = 0;
let audio = new Audio();
let patient = null;

const boxRef = $('#dotBox');
const dotRef = $('#dot');
const colorQueue = ['red', 'green', 'blue', 'yellow'];
const coordinates = 20;

let animation = null;
let colorIndex = 0;
let directionDuringLinearMovement = "right";
let position = { x: 0, y: coordinates };

const setPatient = (value) => {
  patient = parseInt(value);
};

const assignRandomXY = () => {
  let { height, width } = getContainerDemensions();
  const random_y = [ ...Array(50).keys() ].map(i => randomIntFromInterval(1, height));
  const random_x = [ ...Array(50).keys() ].map(i => randomIntFromInterval(1, width));
  settings['random_x'] = random_x;
  settings['random_y'] = random_y;
};

const getContainerDemensions = () => {
  const height = boxRef[0].clientHeight - dotRef[0].clientHeight - coordinates;
  const width = boxRef[0].clientWidth - dotRef[0].clientHeight - coordinates;
  return { height, width };
};

const randomIntFromInterval = (min, max) => {
  return Math.floor(Math.random() * (max - min + 1) + min);
};

const getNext8ShapeLocation = () => {
  const {height, width} = getContainerDemensions();
  let x, y = 0
  if (position.x === coordinates) {
    if (position.y === coordinates) {
      x = width
      y = height
    }
    if(position.y === height){
      x = coordinates
      y = coordinates
    }
  }
  if (position.x === width) {
    if (position.y === height) {
      x = width
      y = coordinates
    }
    if (position.y === coordinates) {
      x = coordinates
      y = height
    }
  }
  
  if (x === undefined || y === undefined) {
    x = width
    y = height
  }
  return {x, y}
};

const getNextRandomLocation = () => {
  let x = settings.random_x[randomIdx];
  let y = settings.random_y[randomIdx];
  randomIdx += 1;
  return {x, y}
};

const getNextLinearLocation = () => {
  const {height, width} = getContainerDemensions();
  let x, y = 0;
  y = Math.floor(height / 2)
  x = position.x >= width ? coordinates : width
  return {x, y}
};

const getNextDiagonalLocation = () => {
  const {height, width} = getContainerDemensions();
  let x,y = 0
  if(position.x === coordinates && position.y === height){
    x = width
    y = coordinates
  }
  if(position.x === width && position.y === coordinates){
    x = coordinates
    y = height
  }
  if(x === undefined || y === undefined){
    x = coordinates
    y = height
  }
  return {x,y}
};

const getNextDiagonalFlippedLocation = () => {
  const {height, width} = getContainerDemensions();
  let x,y = 0
  if(position.x === coordinates && position.y === coordinates){
    x = width
    y = height
  }
  if(position.x === width && position.y === height){
    x = coordinates
    y = coordinates
  }
  if(x === undefined || y === undefined){
    x = coordinates
    y = coordinates
  }
  return {x,y}
};

const getNextDiamondLocation = () => {
  const {height, width} = getContainerDemensions();
  let x,y = 0
  const midY = Math.floor(height/2)
  const midX = Math.floor(width/2)
  if(position.x === midX && position.y === coordinates){
    x = width
    y = midY
  }
  if(position.x === width && position.y === midY){
    x = midX
    y = height
  }
  if(position.x === midX && position.y === height){
    x = coordinates
    y = midY
  }
  if(position.x === coordinates && position.y === midY){
    x = midX
    y = coordinates
  }
  if(x === undefined || y === undefined){
    x = midX
    y = coordinates
  }
  return {x,y}
};

const getNewLocation = () => {
  const {width} = getContainerDemensions();
  
  let newLocation = { x: 0, y: Math.floor(width / 2)};
  const mapping = {
    'emdr-linear': getNextLinearLocation,
    'emdr-non-linear': getNext8ShapeLocation,
    'random': getNextRandomLocation,
    'diamond': getNextDiamondLocation,
    'diagonal': getNextDiagonalLocation,
    'diagonal-flipped': getNextDiagonalFlippedLocation
  };
  if (mapping.hasOwnProperty(settings.mode)) {
    newLocation = mapping[settings.mode]();
  }
  return newLocation;
};

const moveOnce = () => {
  // Pick a new spot on the page
  const next = getNewLocation();
  
  dotRef.animate(
    {
      left:`${next.x}px`,
      top: `${next.y}px`
    },
    {
      duration: (1200 - settings.speed), // in milliseconds
      easing: 'swing', // easing
      start: (amt) => {
        animation = amt;
      },
      step: (now, tween) => {
        const newSpeed = (1200 - settings.speed);
        const reducerPercentage = 0.25;
        animation.duration =  newSpeed - ( settings.speed * reducerPercentage );
        
        const { width } = getContainerDemensions();
        
        if (tween.prop === 'left') {
          if (tween.end > width) {
            tween.end = width - coordinates
          }
          if (tween.end < width) {
            if (settings.mode !== 'random' && settings.mode !== 'diamond' && next.x !== coordinates && next.x < width) {
              tween.end = width;
              animation.duration = 0;
            }
          }
        }
      },
      done: () => {
        moveOnce();
        if(settings.mode === 'emdr-linear') {
          directionDuringLinearMovement = directionDuringLinearMovement === 'left'? 'right' : 'left'
        }
      }
    }
  )
  // Save this new position ready for the next call.
  position = next;
}

const makeStyle = () => {
  // Make style
  dotRef.css('height', `${settings.size}px`);
  dotRef.css('width', `${settings.size}px`);
  dotRef.css('border-radius', "50%");
  dotRef.css('background', "#EC649A");
  dotRef.css('position', "absolute");
  
  boxRef.css('height', "100%");
  boxRef.css('width', "100%");
  boxRef.css('minHeight', "20rem");
  boxRef.css('position', "relative");
  boxRef.css('background', '#FFFFFF');
}

const srcAudio = (filename) => {
  audio.src = filename;
};

const startAudio = () => {
  audio.play();
};

const stopAudio = () => {
  audio.pause();
};

const start = () => {
  if (isRunning) {
    return;
  }
  moveOnce();
  isRunning = true;
  startAudio();
}

const stop = () => {
  dotRef.clearQueue();
  dotRef.delay(2000).stop();
  isRunning = false;
  stopAudio();
};

const bgLoader = (bg) => {
  if (bg.indexOf("#") === 0) {
    return bg;
  }
  else {
    const bgs = {
      "practice": "https://adoring-jennings-b00c99.netlify.app/img/practice.jpg",
      "forrest": "https://adoring-jennings-b00c99.netlify.app/img/forrest.jpg",
      "mountains": "https://adoring-jennings-b00c99.netlify.app/img/mountains.jpg",
      "beach": "https://adoring-jennings-b00c99.netlify.app/img/beach.jpg",
      "hospital": "https://adoring-jennings-b00c99.netlify.app/img/hospital.jpg"
    };
    return `url(${bgs[bg]}) no-repeat center center / cover`;
  }
}

const startRemote = () => {
  let payload = settings;
  payload["status"] = isRunning ? "RUNNING" : "STOP";
  socket.send(JSON.stringify(payload));
};

const reloadRemote = (key) => {
  let payload = settings;
  payload["key"] = key;
  socket.send(JSON.stringify(payload));
};

// Settings: Setter and Getter
const setSettings = () => {
  settings = {
    size: $("#size").val() || 30,
    speed: parseInt($("#speed").val()),
    color: $("#color").is(":checked") || false,
    mode: $("#mode").val() || 'emdr-linear',
    bg: bgLoader($("#bg").val() || '#FFFFFF'),
    sound: $("#sound").val() || '',
    random_x: settings.random_x,
    random_y: settings.random_y
  };
  settings["patient"] = patient;
};

$(document).ready(() => {
  // Reset setting to default
  setSettings();
  $("#cpanel").trigger('reset');
  
  // Init random X and Y
  assignRandomXY();
  
  // Handle input changes
  $("#size").change((e) => {
    setSettings();
    reloadRemote("size");
    dotRef.css("height", settings.size+'px');
    dotRef.css("width", settings.size+'px');
  });
  $("#speed").change((e) => {
    setSettings();
    reloadRemote("speed");
    stop();
    dotRef.animate({
      duration: 3000
    });
    start();
  });
  $("#color").change((e) => {
    setSettings();
    reloadRemote("color");
    if (settings.color) {
      let colorLoop = setInterval(() => {
        if (colorIndex === colorQueue.length) {
          colorIndex = 0;
        }
        dotRef.css('background', colorQueue[colorIndex]);
        colorIndex += 1;
      }, 800);
      localStorage.setItem('colorLoop', colorLoop);
    }
    else {
      colorIndex = 0;
      clearInterval(localStorage.getItem('colorLoop'));
      localStorage.removeItem('colorLoop');
      dotRef.css('background', '#EC649A');
    }
  });
  $("#mode").change((e) => {
    setSettings();
    if (!isRunning) {
      return;
    }
    stop();
    reloadRemote("mode");
    const {height, width} = getContainerDemensions();
    if (settings.mode === 'emdr-non-linear' || settings.mode === 'diagonal-flipped') {
      position = {x: coordinates, y: coordinates};
    }
    else if (settings.mode === 'diamond') {
      position = {x: Math.floor(width / 2), y: coordinates};
    }
    else if (settings.mode === 'diagonal') {
      position = {x: coordinates, y: height};
    }
    else if (settings.mode === 'emdr-linear') {
      position = {x: coordinates, y: Math.floor(height / 2)};
    }
    dotRef.animate(
      {
        left: `${position.x}px`,
        top: `${position.y}px`
      },
      {
        duration: (1200 - settings.speed), // in milliseconds
        easing: 'swing'
      }
    );
    start();
  });
  $("#bg").change((e) => {
    setSettings();
    reloadRemote("bg");
    boxRef.css('background', settings.bg);
  });
  $("#sound").change((e) => {
    setSettings();
    reloadRemote("sound");
    
    srcAudio(settings.sound);
    // play music
    if (settings.sound !== "") {
      if (!isRunning) {
        return;
      }
      stopAudio();
      startAudio();
    }
    else {
      stopAudio();
    }
    // end play music
  });
  
  $("#runDot").click((e) => {
    if (isRunning) { stop(); }
    else { start(); }
    $(e.currentTarget).text(isRunning ? 'Stop' : 'Start');
    startRemote();
  });
  
  // end Handle
  
  /*
  * SOCKET SETTINGS
  * */
  socket = new WebSocket('ws://' + window.location.host + '/ws/asgi/');
  
  socket.onopen = (e) => {
    console.log('WebSockets connection created.');
  };
  
  socket.onmessage = (e) => {
    const data = JSON.parse(e.data);
  };
});