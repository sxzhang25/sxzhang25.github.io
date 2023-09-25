svgs = document.getElementsByTagName('svg')
for (let i = 0; i < svgs.length; i++) {
    svgs[i].addEventListener("load", () => {
        // svgName = svgs[i].parentNode.getAttribute('id').split('-')[0]

        svgs[i].setCurrentTime(0)
        // edge cases
        // if (svgName.substring(0, 5) == 'logo3') {
        //     svgs[i].setCurrentTime(6)
        // }
        // if (svgName.substring(0, 8) == 'shapes38') {
        //     svgs[i].setCurrentTime(3)
        // }
        svgs[i].pauseAnimations()

        // display SVG code
        // containerID = svgName + '-text'
        // container = document.getElementById(containerID)
        // if (container != null) {
        //     container.textContent = svgs[i].outerHTML
        //     hljs.highlightElement(container);
        // }
    }, false);
}

let playSVG = (svgDivId) => {
    console.log(svgDivId)
    let svgDivElement = document.getElementById(svgDivId)
    console.log(svgDivElement)
    // let svgElement = document.getElementById(svgDivId)
    let svgElement = svgDivElement.contentDocument.children[0]
    console.log(svgElement)
    svgElement.setCurrentTime(0)
    svgElement.unpauseAnimations()
}

// let play_with_audio = (svgDivId, audioId) => {
//     let audio = document.getElementById(audioId);
//     audio.currentTime = 0;
//     audio.play();
//     playSVG(svgDivId)
// }

// let limit_play_time = (e, time_limit) => {
//     if (e.currentTime > time_limit) {
//         e.pause();
//     }
// }

// hljs.highlightAll();

// document.addEventListener("DOMContentLoaded", () => {
//     tts = document.getElementsByTagName('tt');
//     for (let i = 0; i < tts.length; i++) {
//         tt = tts[i]
//         ttString = tt.innerText;
//         tt.innerHTML = null
//         let a = document.createElement('a');
//         tt.appendChild(a);
//         a.href = "./assets/pdf/supplemental.pdf";
//         a.innerText = ttString
//     }
// });